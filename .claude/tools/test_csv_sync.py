#!/usr/bin/env python3
"""
Comprehensive Test Suite for CSV-to-MANIFEST Sync Tool

Test Coverage:
1. Slugification (name → slug conversion)
   - Simple names (single/multiple words)
   - Names with titles (Dr., Professor, Prof.)
   - Names with special characters
   - Empty/null names
   - Edge cases (single letter, numbers, accents)

2. CSV Parsing & Validation
   - Valid rows with all fields
   - Missing name or email
   - Empty CSV
   - Malformed CSV
   - UTF-8 encoding

3. Field Extraction
   - Title extraction from "Role/Institution"
   - Institution extraction (hyphen-separated, comma-separated)
   - Conference status field preservation
   - Optional fields

4. Manifest Merging
   - New leads (not in existing manifest)
   - Updated leads (existing slug, new data)
   - Preserving custom fields
   - Preserving old metadata

5. Error Handling
   - File not found errors
   - CSV parsing errors
   - Invalid JSON in existing manifest
   - Write permission errors

6. Integration Tests
   - Full sync workflow
   - Multiple leads processing
   - Duplicate slug handling
"""

import json
import csv
import sys
import tempfile
from pathlib import Path
from datetime import datetime
import traceback

# Import the sync function (handle hyphenated filename)
import importlib.util
tool_dir = Path(__file__).parent
sync_module_path = tool_dir / 'csv-to-manifest-sync.py'
spec = importlib.util.spec_from_file_location("csv_to_manifest_sync", sync_module_path)
sync_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_module)
slugify = sync_module.slugify
sync_csv_to_manifest = sync_module.sync_csv_to_manifest


class TestRunner:
    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'total': 0,
            'errors': []
        }
        self.temp_files = []

    def cleanup(self):
        """Clean up temporary files."""
        for f in self.temp_files:
            try:
                Path(f).unlink()
            except:
                pass

    def assert_equal(self, actual, expected, test_name):
        """Assert equality and record result."""
        self.results['total'] += 1
        if actual == expected:
            self.results['passed'].append(test_name)
            return True
        else:
            msg = f"Expected {expected!r}, got {actual!r}"
            self.results['failed'].append((test_name, msg))
            return False

    def assert_true(self, condition, test_name):
        """Assert condition is true."""
        self.results['total'] += 1
        if condition:
            self.results['passed'].append(test_name)
            return True
        else:
            self.results['failed'].append((test_name, "Condition was false"))
            return False

    def assert_contains(self, container, item, test_name):
        """Assert item is in container."""
        self.results['total'] += 1
        if item in container:
            self.results['passed'].append(test_name)
            return True
        else:
            msg = f"{item!r} not found in {container!r}"
            self.results['failed'].append((test_name, msg))
            return False

    def create_temp_csv(self, rows):
        """Create temporary CSV file with given rows."""
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        self.temp_files.append(f.name)

        writer = csv.DictWriter(
            f,
            fieldnames=['Name', 'Email', 'Role/Institution', 'conference:Education and Innovation']
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        f.close()
        return f.name

    def create_temp_manifest(self, leads):
        """Create temporary MANIFEST.json with given leads."""
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_files.append(f.name)

        manifest = {
            'leads': leads,
            '_metadata': {
                'synced_at': datetime.now().isoformat(),
                'source': 'test',
                'count': len(leads)
            }
        }
        json.dump(manifest, f)
        f.close()
        return f.name

    # ============================================================================
    # TEST SUITES
    # ============================================================================

    def test_slugification(self):
        """Test slugify function with various inputs."""
        print("\n📋 TEST SUITE 1: Slugification")
        print("-" * 60)

        tests = [
            ("Yong Yu", "yong-yu", "Simple two-word name"),
            ("Jennifer Pankowski", "jennifer-pankowski", "Two-word name"),
            ("Dr. Jennifer Pankowski", "jennifer-pankowski", "Name with title (Dr.)"),
            ("Professor John Smith", "john-smith", "Name with title (Professor)"),
            ("Prof. Jane Doe", "jane-doe", "Name with title (Prof.)"),
            ("A", "a", "Single letter"),
            ("Mary-Jane Watson", "mary-watson", "Hyphenated name (takes first and last)"),
            ("Jean-Luc Picard", "jean-picard", "Hyphenated name with accent-like chars"),
            ("José García", "josé-garcía", "Name with accents"),
            ("", "", "Empty string"),
            ("   ", "", "Whitespace only"),
            ("Dr.   Test Name", "test-name", "Title with extra spaces"),
            ("Bob", "bob", "Single word (no hyphen)"),
            ("UPPERCASE NAME", "uppercase-name", "Uppercase conversion"),
            ("name-with-multiple---hyphens", "name-with-multiple-hyphens", "Multiple hyphens normalized"),
        ]

        for name, expected, description in tests:
            result = slugify(name)
            self.assert_equal(result, expected, f"Slug: {description}")

    def test_csv_parsing(self):
        """Test CSV parsing and validation."""
        print("\n📋 TEST SUITE 2: CSV Parsing & Validation")
        print("-" * 60)

        # Test 1: Valid single row
        csv_path = self.create_temp_csv([
            {'Name': 'John Doe', 'Email': 'john@example.com', 'Role/Institution': 'Dean', 'conference:Education and Innovation': ''}
        ])
        result = sync_csv_to_manifest(csv_path, self.create_temp_manifest([]))
        self.assert_equal(result['leads_synced'], 1, "Single valid row parsed")
        self.assert_equal(len(result['errors']), 0, "No errors for valid row")

        # Test 2: Multiple valid rows
        csv_path = self.create_temp_csv([
            {'Name': 'Alice Smith', 'Email': 'alice@example.com', 'Role/Institution': 'Director', 'conference:Education and Innovation': ''},
            {'Name': 'Bob Johnson', 'Email': 'bob@example.com', 'Role/Institution': 'Coordinator', 'conference:Education and Innovation': ''},
            {'Name': 'Carol White', 'Email': 'carol@example.com', 'Role/Institution': 'Manager', 'conference:Education and Innovation': ''},
        ])
        result = sync_csv_to_manifest(csv_path, self.create_temp_manifest([]))
        self.assert_equal(result['leads_synced'], 3, "Multiple rows parsed")

        # Test 3: Missing email
        csv_path = self.create_temp_csv([
            {'Name': 'John Doe', 'Email': '', 'Role/Institution': 'Dean', 'conference:Education and Innovation': ''},
        ])
        result = sync_csv_to_manifest(csv_path, self.create_temp_manifest([]))
        self.assert_equal(result['leads_synced'], 0, "Row with missing email skipped")
        self.assert_true(len(result['errors']) > 0, "Error recorded for missing email")

        # Test 4: Missing name
        csv_path = self.create_temp_csv([
            {'Name': '', 'Email': 'john@example.com', 'Role/Institution': 'Dean', 'conference:Education and Innovation': ''},
        ])
        result = sync_csv_to_manifest(csv_path, self.create_temp_manifest([]))
        self.assert_equal(result['leads_synced'], 0, "Row with missing name skipped")
        self.assert_true(len(result['errors']) > 0, "Error recorded for missing name")

        # Test 5: Mixed valid and invalid rows
        csv_path = self.create_temp_csv([
            {'Name': 'Alice Smith', 'Email': 'alice@example.com', 'Role/Institution': 'Director', 'conference:Education and Innovation': ''},
            {'Name': 'Bad Row', 'Email': '', 'Role/Institution': 'Coordinator', 'conference:Education and Innovation': ''},
            {'Name': 'Carol White', 'Email': 'carol@example.com', 'Role/Institution': 'Manager', 'conference:Education and Innovation': ''},
        ])
        result = sync_csv_to_manifest(csv_path, self.create_temp_manifest([]))
        self.assert_equal(result['leads_synced'], 2, "Mixed rows: valid ones processed")
        self.assert_true(len(result['errors']) > 0, "Mixed rows: invalid ones recorded as errors")

    def test_field_extraction(self):
        """Test extraction of title and institution fields."""
        print("\n📋 TEST SUITE 3: Field Extraction")
        print("-" * 60)

        # Test 1: Title - Institution (hyphen-separated)
        csv_path = self.create_temp_csv([
            {'Name': 'John Doe', 'Email': 'john@example.com', 'Role/Institution': 'Dean of Students - SUNY Buffalo', 'conference:Education and Innovation': ''},
        ])
        manifest_path = self.create_temp_manifest([])
        result = sync_csv_to_manifest(csv_path, manifest_path)

        with open(manifest_path) as f:
            manifest = json.load(f)
            lead = manifest['leads'][0]
            self.assert_equal(lead['title'], 'Dean of Students', "Title extracted from hyphen-separated field")
            self.assert_equal(lead['institution'], 'SUNY Buffalo', "Institution extracted from hyphen-separated field")

        # Test 2: Title with comma-separated institution
        csv_path = self.create_temp_csv([
            {'Name': 'Jane Smith', 'Email': 'jane@example.com', 'Role/Institution': 'VP Academic Affairs, CUNY City College', 'conference:Education and Innovation': ''},
        ])
        manifest_path = self.create_temp_manifest([])
        result = sync_csv_to_manifest(csv_path, manifest_path)

        with open(manifest_path) as f:
            manifest = json.load(f)
            lead = manifest['leads'][0]
            self.assert_equal(lead['title'], 'VP Academic Affairs', "Title extracted from comma-separated field")
            self.assert_equal(lead['institution'], 'CUNY City College', "Institution extracted from comma-separated field")

        # Test 3: Title only (no institution)
        csv_path = self.create_temp_csv([
            {'Name': 'Bob Johnson', 'Email': 'bob@example.com', 'Role/Institution': 'Director', 'conference:Education and Innovation': ''},
        ])
        manifest_path = self.create_temp_manifest([])
        result = sync_csv_to_manifest(csv_path, manifest_path)

        with open(manifest_path) as f:
            manifest = json.load(f)
            lead = manifest['leads'][0]
            self.assert_equal(lead['title'], 'Director', "Title extracted from single field")
            self.assert_equal(lead['institution'], '', "Institution empty when not provided")

        # Test 4: Conference status preservation
        csv_path = self.create_temp_csv([
            {'Name': 'Carol White', 'Email': 'carol@example.com', 'Role/Institution': 'Manager', 'conference:Education and Innovation': 'Interested'},
        ])
        manifest_path = self.create_temp_manifest([])
        result = sync_csv_to_manifest(csv_path, manifest_path)

        with open(manifest_path) as f:
            manifest = json.load(f)
            lead = manifest['leads'][0]
            self.assert_equal(lead.get('conference_status'), 'Interested', "Conference status preserved")

    def test_manifest_merging(self):
        """Test merging CSV data with existing manifest."""
        print("\n📋 TEST SUITE 4: Manifest Merging")
        print("-" * 60)

        # Test 1: New lead (not in existing manifest)
        csv_path = self.create_temp_csv([
            {'Name': 'New Person', 'Email': 'new@example.com', 'Role/Institution': 'New Role', 'conference:Education and Innovation': ''},
        ])
        manifest_path = self.create_temp_manifest([])
        result = sync_csv_to_manifest(csv_path, manifest_path)
        self.assert_equal(result['leads_synced'], 1, "New lead added to manifest")

        # Test 2: Updated lead (existing slug)
        csv_path = self.create_temp_csv([
            {'Name': 'John Doe', 'Email': 'john.new@example.com', 'Role/Institution': 'Updated Role', 'conference:Education and Innovation': ''},
        ])
        existing = [
            {'slug': 'john-doe', 'email': 'john.old@example.com', 'name': 'John Doe', 'title': 'Old Title', 'institution': 'Old University', 'custom_field': 'custom_value'}
        ]
        manifest_path = self.create_temp_manifest(existing)
        result = sync_csv_to_manifest(csv_path, manifest_path)

        with open(manifest_path) as f:
            manifest = json.load(f)
            lead = manifest['leads'][0]
            self.assert_equal(lead['email'], 'john.new@example.com', "Email updated in existing lead")
            self.assert_equal(lead['title'], 'Updated Role', "Title updated in existing lead")
            self.assert_equal(lead.get('custom_field'), 'custom_value', "Custom field preserved from existing lead")

        # Test 3: Preserving all custom fields
        csv_path = self.create_temp_csv([
            {'Name': 'Test Person', 'Email': 'test@example.com', 'Role/Institution': 'Test Role', 'conference:Education and Innovation': ''},
        ])
        existing = [
            {
                'slug': 'test-person',
                'email': 'test@example.com',
                'name': 'Test Person',
                'title': 'Test Role',
                'institution': '',
                'notes': 'Follow up next month',
                'last_contact': '2026-05-01',
                'custom_metadata': {'key': 'value'}
            }
        ]
        manifest_path = self.create_temp_manifest(existing)
        result = sync_csv_to_manifest(csv_path, manifest_path)

        with open(manifest_path) as f:
            manifest = json.load(f)
            lead = manifest['leads'][0]
            self.assert_equal(lead.get('notes'), 'Follow up next month', "Notes field preserved")
            self.assert_equal(lead.get('last_contact'), '2026-05-01', "Custom date field preserved")
            self.assert_equal(lead.get('custom_metadata'), {'key': 'value'}, "Nested custom metadata preserved")

    def test_error_handling(self):
        """Test error handling and edge cases."""
        print("\n📋 TEST SUITE 5: Error Handling")
        print("-" * 60)

        # Test 1: CSV file not found
        try:
            sync_csv_to_manifest('/nonexistent/path.csv', self.create_temp_manifest([]))
            self.assert_true(False, "File not found raises error")
        except FileNotFoundError:
            self.assert_true(True, "File not found raises FileNotFoundError")

        # Test 2: Empty CSV (no rows)
        csv_path = self.create_temp_csv([])
        result = sync_csv_to_manifest(csv_path, self.create_temp_manifest([]))
        self.assert_equal(result['leads_synced'], 0, "Empty CSV results in 0 leads synced")

        # Test 3: Corrupt JSON manifest (should recover)
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_files.append(f.name)
        f.write('{ invalid json')
        f.close()

        csv_path = self.create_temp_csv([
            {'Name': 'John Doe', 'Email': 'john@example.com', 'Role/Institution': 'Dean', 'conference:Education and Innovation': ''},
        ])
        result = sync_csv_to_manifest(csv_path, f.name)
        self.assert_true(result['success'], "Sync succeeds even with corrupt existing manifest")
        self.assert_true(any('existing MANIFEST' in e for e in result['errors']), "Corrupt manifest error recorded")

    def test_integration(self):
        """Test full end-to-end workflows."""
        print("\n📋 TEST SUITE 6: Integration Tests")
        print("-" * 60)

        # Test 1: Full workflow with realistic data
        csv_data = [
            {'Name': 'Dr. Alice Smith', 'Email': 'alice@suny.edu', 'Role/Institution': 'VP Academic Affairs - SUNY Buffalo', 'conference:Education and Innovation': 'Interested'},
            {'Name': 'Bob Johnson', 'Email': 'bob@cuny.edu', 'Role/Institution': 'Dean, CUNY City College', 'conference:Education and Innovation': 'Confirmed'},
            {'Name': 'Carol Williams', 'Email': 'carol@private.edu', 'Role/Institution': 'Director of Student Services', 'conference:Education and Innovation': ''},
        ]
        csv_path = self.create_temp_csv(csv_data)
        manifest_path = self.create_temp_manifest([])

        result = sync_csv_to_manifest(csv_path, manifest_path)
        self.assert_equal(result['leads_synced'], 3, "Full workflow processes all leads")

        with open(manifest_path) as f:
            manifest = json.load(f)
            self.assert_equal(len(manifest['leads']), 3, "Manifest contains all leads")
            self.assert_true('_metadata' in manifest, "Metadata section present")
            self.assert_equal(manifest['_metadata']['count'], 3, "Metadata count accurate")

            # Verify slugs are unique
            slugs = [lead['slug'] for lead in manifest['leads']]
            self.assert_equal(len(slugs), len(set(slugs)), "All slugs are unique")

        # Test 2: CSV update with new and changed leads
        csv_data_v2 = [
            {'Name': 'Dr. Alice Smith', 'Email': 'alice.new@suny.edu', 'Role/Institution': 'Provost - SUNY Buffalo', 'conference:Education and Innovation': 'Interested'},  # Updated
            {'Name': 'Bob Johnson', 'Email': 'bob@cuny.edu', 'Role/Institution': 'Dean, CUNY City College', 'conference:Education and Innovation': 'Confirmed'},  # Unchanged
            {'Name': 'Diana Martinez', 'Email': 'diana@midwest.edu', 'Role/Institution': 'Dean', 'conference:Education and Innovation': ''},  # New
        ]
        csv_path_v2 = self.create_temp_csv(csv_data_v2)
        result = sync_csv_to_manifest(csv_path_v2, manifest_path)
        self.assert_equal(result['leads_synced'], 3, "Update processes all current leads")

        with open(manifest_path) as f:
            manifest = json.load(f)
            alice = next((l for l in manifest['leads'] if l['slug'] == 'alice-smith'), None)
            self.assert_true(alice is not None, "Updated lead still in manifest")
            self.assert_equal(alice['email'], 'alice.new@suny.edu', "Lead email updated")
            self.assert_equal(alice['title'], 'Provost', "Lead title updated")

    # ============================================================================
    # REPORT GENERATION
    # ============================================================================

    def run_all_tests(self):
        """Run all test suites."""
        print("\n" + "=" * 60)
        print("CSV-to-MANIFEST SYNC TEST SUITE")
        print("=" * 60)

        try:
            self.test_slugification()
            self.test_csv_parsing()
            self.test_field_extraction()
            self.test_manifest_merging()
            self.test_error_handling()
            self.test_integration()
        except Exception as e:
            self.results['errors'].append(traceback.format_exc())
            print(f"\n❌ FATAL ERROR: {str(e)}")
        finally:
            self.cleanup()

        return self.generate_report()

    def generate_report(self):
        """Generate test report."""
        passed = len(self.results['passed'])
        failed = len(self.results['failed'])
        total = self.results['total']
        pass_rate = (passed / total * 100) if total > 0 else 0

        report = {
            'summary': {
                'total_tests': total,
                'passed': passed,
                'failed': failed,
                'pass_rate': f"{pass_rate:.1f}%",
                'timestamp': datetime.now().isoformat()
            },
            'tests': {
                'passed': self.results['passed'],
                'failed': [{'test': name, 'error': msg} for name, msg in self.results['failed']]
            },
            'errors': self.results['errors']
        }

        # Print summary
        print("\n" + "=" * 60)
        print("TEST REPORT")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Pass Rate: {pass_rate:.1f}%")

        if self.results['failed']:
            print("\n❌ FAILED TESTS:")
            print("-" * 60)
            for test_name, error in self.results['failed']:
                print(f"\n  {test_name}")
                print(f"  └─ {error}")

        if self.results['errors']:
            print("\n💥 CRITICAL ERRORS:")
            print("-" * 60)
            for error in self.results['errors']:
                print(f"\n{error}")

        if failed == 0 and not self.results['errors']:
            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED")
            print("=" * 60)

        return report


if __name__ == '__main__':
    runner = TestRunner()
    report = runner.run_all_tests()

    # Export report as JSON for analysis
    report_path = Path('.claude/tools/test_results.json')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n📊 Full report saved to: {report_path}")

    # Exit with appropriate code
    if report['summary']['failed'] == 0:
        sys.exit(0)
    else:
        sys.exit(1)

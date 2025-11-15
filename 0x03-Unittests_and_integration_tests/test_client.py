#!/usr/bin/env python3
"""Unit tests and integration tests for the client module."""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the expected value."""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        mock_org.return_value = test_payload
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos."""
        test_payload = [
            {"name": "episodes.dart"},
            {"name": "kratu"},
        ]
        mock_get_json.return_value = test_payload
        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos")
            client = GithubOrgClient("google")
            result = client.public_repos()
            self.assertEqual(result, ["episodes.dart", "kratu"])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos")
            mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license",
         False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean value."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test cases for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running integration tests."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures after running integration tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method in integration test."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos)

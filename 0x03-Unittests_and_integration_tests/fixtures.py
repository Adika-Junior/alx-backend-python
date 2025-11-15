#!/usr/bin/env python3
"""Test fixtures for integration testing of GitHub organization client."""
org_payload = {
    "login": "google",
    "id": 1342004,
    "url": "https://api.github.com/orgs/google",
    "repos_url": "https://api.github.com/orgs/google/repos",
    "events_url": "https://api.github.com/orgs/google/events",
    "hooks_url": "https://api.github.com/orgs/google/hooks",
    "issues_url": "https://api.github.com/orgs/google/issues",
    "members_url": "https://api.github.com/orgs/google/members{/member}",
    "public_members_url": "https://api.github.com/orgs/google/public_members{/member}",
    "avatar_url": "https://avatars1.githubusercontent.com/u/1342004?v=4",
    "description": None,
}

repos_payload = [
    {
        "id": 7697149,
        "name": "episodes.dart",
        "private": False,
        "owner": {
            "login": "google",
            "id": 1342004,
        },
        "fork": False,
        "url": "https://api.github.com/repos/google/episodes.dart",
        "created_at": "2013-01-19T00:31:37Z",
        "updated_at": "2019-09-23T11:53:58Z",
        "has_issues": True,
        "forks": 0,
        "default_branch": "master",
        "license": {
            "key": "apache-2.0",
            "name": "Apache License 2.0",
            "spdx_id": "Apache-2.0",
            "url": "https://api.github.com/licenses/apache-2.0",
            "node_id": "MDc6TGljZW5zZTI=",
        },
    },
    {
        "id": 8566972,
        "name": "kratu",
        "private": False,
        "owner": {
            "login": "google",
            "id": 1342004,
        },
        "fork": False,
        "url": "https://api.github.com/repos/google/kratu",
        "created_at": "2013-03-04T22:52:33Z",
        "updated_at": "2019-11-15T22:22:16Z",
        "has_issues": True,
        "forks": 0,
        "default_branch": "master",
        "license": {
            "key": "apache-2.0",
            "name": "Apache License 2.0",
            "spdx_id": "Apache-2.0",
            "url": "https://api.github.com/licenses/apache-2.0",
            "node_id": "MDc6TGljZW5zZTI=",
        },
    },
]

expected_repos = [
    "episodes.dart",
    "kratu",
]

apache2_repos = [
    "episodes.dart",
    "kratu",
]


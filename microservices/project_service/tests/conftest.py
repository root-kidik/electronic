import pathlib
import sys

import pytest
import grpc

from testsuite.databases.pgsql import discover

USERVER_CONFIG_HOOKS = ["_prepare_service_config"]
pytest_plugins = [
    "pytest_userver.plugins.postgresql",
    "pytest_userver.plugins.grpc",
]


@pytest.fixture(scope="session")
def projects_protos():
    return grpc.protos("project_service.proto")


@pytest.fixture(scope="session")
def project_services():
    return grpc.services("project_service.proto")


@pytest.fixture
def grpc_service(pgsql, project_services, grpc_channel, service_client):
    return project_services.ProjectServiceStub(grpc_channel)


@pytest.fixture(scope="session")
def mock_grpc_project_session(
    project_services,
    grpc_mockserver,
    create_grpc_mock,
):
    mock = create_grpc_mock(project_services.ProjectServiceServicer)
    project_services.add_ProjectServiceServicer_to_server(
        mock.servicer,
        grpc_mockserver,
    )
    return mock


@pytest.fixture
def mock_grpc_server(mock_grpc_project_session):
    with mock_grpc_project_session.mock() as mock:
        yield mock


@pytest.fixture(scope="session")
def _prepare_service_config(grpc_mockserver_endpoint):
    def patch_config(config, config_vars):
        components = config["components_manager"]["components"]

    return patch_config


def pytest_configure(config):
    sys.path.append(str(pathlib.Path(__file__).parent.parent / "proto/api/"))


@pytest.fixture(scope="session")
def service_source_dir():
    """Path to root directory service."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture(scope="session")
def initial_data_path(service_source_dir):
    """Path for find files with data"""
    return [
        service_source_dir / "postgresql/data",
    ]


@pytest.fixture(scope="session")
def pgsql_local(service_source_dir, pgsql_local_create):
    """Create schemas databases for tests"""
    databases = discover.find_schemas(
        "project_service",
        [service_source_dir.joinpath("postgresql/schemas")],
    )
    return pgsql_local_create(list(databases.values()))

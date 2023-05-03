from worker.application import RegisterUserUseCase, MongoService, LoginUserUseCase
from shared.infrastructure import MongoDatabase, Settings
from worker.infrastructure import MongoWorkerRepository
from dependency_injector import containers, providers
from contextlib import contextmanager
from typing import Optional


class RepositoriesContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(Settings)
    mongo_db = providers.Singleton(
        MongoDatabase,
        db_uri=settings.provided.MONGO_URI,
        max_pool_size=settings.provided.MONGO_MAX_POOL_SIZE,
        timeout=settings.provided.MONGO_TIMEOUT_MS
    )
    mongo_worker_repository = providers.Singleton(MongoWorkerRepository, session_factory=mongo_db.provided.session)


class ServicesContainer(containers.DeclarativeContainer):
    repositories: RepositoriesContainer = providers.DependenciesContainer()
    mongo_service = providers.Factory(MongoService, mongo_repository=repositories.mongo_worker_repository)


class UseCasesContainer(containers.DeclarativeContainer):
    services: ServicesContainer = providers.DependenciesContainer()
    settings = providers.Dependency(Settings)
    register_user = providers.Factory(RegisterUserUseCase, mongo_service=services.mongo_service)
    login_user = providers.Factory(LoginUserUseCase, mongo_service=services.mongo_service)


class AppContainer(containers.DeclarativeContainer):
    settings = providers.ThreadSafeSingleton(Settings)
    repositories = providers.Container(RepositoriesContainer, settings=settings)
    services = providers.Container(ServicesContainer, repositories=repositories)
    usecases = providers.Container(UseCasesContainer, services=services, settings=settings)


class SingletonContainer:
    container: Optional[AppContainer] = None

    @classmethod
    @contextmanager
    def scope(cls):
        try:
            cls.container.services.init_resources()
            yield cls.container
        finally:
            cls.container.services.shutdown_resources()

    @classmethod
    def init(cls):
        if cls.container is None:
            cls.container = AppContainer()

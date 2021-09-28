from ._types import Options, Project, ProjectResponse, UpdateResponse
from ._utils import _request


class Projects:
    _root = "/projects"

    def __init__(self, options: Options) -> None:
        self.options = options

    async def list(self) -> ProjectResponse:
        """Returns all projects accessible by the API key."""
        return await _request(self._root, self.options)

    async def get(self, project_id: str) -> Project:
        """Retrieves a specific project based on the provided projectId."""
        return await _request(f'{self._root}/{project_id}', self.options)

    async def create(self, name: str) -> Project:
        """Creates a project."""
        return await _request(
            self._root, self.options,
            method='POST', payload={'name': name},
            headers={'Content-Type': 'application/json'}
        )

    async def update(self, project_id: str, name: str = None,
                     company: str = None) -> UpdateResponse:
        """Updates a project's information."""
        payload = {}
        # there's got to be a better way to do this without non-specific kwargs
        if name:
            payload['name'] = name
        if company:
            payload['company'] = company
        return await _request(
            f'{self._root}/{project_id}', self.options,
            method='PATCH', payload=payload,
            headers={'Content-Type': 'application/json'}
        )

    async def delete(self, project_id: str) -> None:
        """Deletes a specific project based on the provided projectId."""
        await _request(
            f'{self._root}/{project_id}', self.options,
            method='DELETE'
        )

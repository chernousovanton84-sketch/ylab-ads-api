import pytest
from rest_framework.test import APIClient
from .models import Author, Ad


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def author(db):
    return Author.objects.create(name="Иван Иванов")


@pytest.fixture
def ad(db, author):
    return Ad.objects.create(
        title="Продам ноутбук",
        description="Отличное состояние",
        price="50000.00",
        status="draft",
        author=author,
    )


@pytest.mark.django_db
class TestAdAPI:
    def test_create_ad(self, api_client, author):
        """Создание объявления — статус draft по умолчанию."""
        response = api_client.post(
            "/api/ads/",
            {
                "title": "Новый товар",
                "description": "Описание",
                "price": "1000.00",
                "author_id": author.id,
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["status"] == "draft"
        assert response.data["title"] == "Новый товар"

    def test_create_ad_without_author(self, api_client):
        """Создание без автора — ошибка 400."""
        response = api_client.post(
            "/api/ads/",
            {
                "title": "Товар",
                "description": "Описание",
                "price": "1000.00",
            },
            format="json",
        )
        assert response.status_code == 400

    def test_list_default_published(self, api_client, ad):
        """По умолчанию — только published."""
        response = api_client.get("/api/ads/")
        assert response.status_code == 200
        assert len(response.data) == 0  # draft не показывается

    def test_list_with_draft_filter(self, api_client, ad):
        """Фильтр status=draft."""
        response = api_client.get("/api/ads/?status=draft")
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_list_invalid_status(self, api_client):
        """Неверный статус — ошибка 400."""
        response = api_client.get("/api/ads/?status=wrong")
        assert response.status_code == 400

    def test_get_ad_by_id(self, api_client, ad):
        """Получение объявления по id."""
        response = api_client.get(f"/api/ads/{ad.id}/")
        assert response.status_code == 200
        assert response.data["title"] == "Продам ноутбук"

    def test_get_ad_404(self, api_client):
        """Несуществующий id — 404."""
        response = api_client.get("/api/ads/9999/")
        assert response.status_code == 404

    def test_patch_status(self, api_client, ad):
        """PATCH меняет статус."""
        response = api_client.patch(
            f"/api/ads/{ad.id}/",
            {"status": "published"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["status"] == "published"

    def test_delete_ad(self, api_client, ad):
        """DELETE удаляет объявление."""
        response = api_client.delete(f"/api/ads/{ad.id}/")
        assert response.status_code == 204
        assert Ad.objects.count() == 0

    def test_search_by_title(self, api_client, ad):
        """Поиск по title (без учёта регистра)."""
        ad.status = "published"
        ad.save()
        response = api_client.get("/api/ads/?search=ноутбук")
        assert response.status_code == 200
        assert len(response.data) == 1

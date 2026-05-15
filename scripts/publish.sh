#!/bin/bash
# Script para publicar manualmente a TestPyPI o PyPI
# Uso: ./scripts/publish.sh [testpypi|pypi]
# Por defecto: testpypi

set -e

REPO=${1:-testpypi}

case "$REPO" in
    testpypi)
        REPO_URL="https://test.pypi.org/legacy/"
        echo "Publicando a TestPyPI..."
        ;;
    pypi)
        REPO_URL="https://upload.pypi.org/legacy/"
        echo "Publicando a PyPI (producción)..."
        ;;
    *)
        echo "Uso: $0 [testpypi|pypi]"
        echo "Ejemplo: $0 testpypi"
        exit 1
        ;;
esac

# Build
echo "Construyendo paquete..."
hatch build

# Publish
echo "Subiendo a $REPO..."
twine upload --repository-url "$REPO_URL" dist/*

echo "✅ Publicación completada a $REPO"

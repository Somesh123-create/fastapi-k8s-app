#!/bin/bash

# Generate migration file

set -e

MIGRATION_NAME=${1:-"new_migration"}

echo "📝 Creating migration: $MIGRATION_NAME"

# Create migration file
alembic revision --autogenerate -m "$MIGRATION_NAME"

echo "✅ Migration created successfully"
echo ""
echo "Next steps:"
echo "1. Review the migration file in app/migrations/versions/"
echo "2. Edit if needed"
echo "3. Run 'make migrate' to apply the migration"
echo ""

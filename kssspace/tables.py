"""
Database tables management.

[[ tables ]]
- author
- giant
- giant_tag
- giant_tag_assoc
"""
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    Boolean,
    UniqueConstraint,
    func,
)

metadata = MetaData()


class ColumnAdder:
    """Provider for general time stamp columns."""

    @staticmethod
    def add_timestamp_and_audit_columns():
        return [
            Column(
                "created_at",
                DateTime,
                nullable=False,
                server_default=func.now(),
                default=func.now(),
            ),
            Column("created_by", ForeignKey("author.id")),
            Column("updated_at", DateTime, onupdate=func.now()),
            Column("updated_by", ForeignKey("author.id")),
            Column("deleted_at", DateTime),
            Column("deleted_by", ForeignKey("author.id")),
        ]


giant = Table(
    "giant",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("description", Text, nullable=False),
    Column("homepage", String),
    Column("github", String),
    Column("twitter_x", String),
    Column("mastodon", String),
    *ColumnAdder.add_timestamp_and_audit_columns(),
    UniqueConstraint("name", name="giant_uq_1"),
)


giant_tag = Table(
    "giant_tag",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    *ColumnAdder.add_timestamp_and_audit_columns(),
)


giant_tag_assoc = Table(
    "giant_tag_assoc",
    metadata,
    Column("giant_id", ForeignKey("giant.id")),
    Column("tag_id", ForeignKey("giant_tag.id")),
    UniqueConstraint("giant_id", "tag_id", name="giant_tag_assoc_uq_1"),
)


author = Table(
    "author",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("ename", String),
    Column("nickname", String),
    *ColumnAdder.add_timestamp_and_audit_columns(),
)


note = Table(
    "note",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100), nullable=False),
    Column("slug", String(255), unique=True),
    Column("summary", Text, nullable=False),
    Column("body", Text),
    Column("thumbnail", String(255)),
    Column("is_draft", Boolean, nullable=False, default=True),
    Column(
        "created_at",
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    ),
    Column("updated_at", DateTime),
)

note_tag = Table(
    "note_tag",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

note_tag_assoc = Table(
    "note_tag_assoc",
    metadata,
    Column("note_id", ForeignKey("note.id")),
    Column("tag_id", ForeignKey("note_tag.id")),
    UniqueConstraint(
        "note_id",
        "tag_id",
        name="note_tag_assoc_uq_1",
    ),
)

series = Table(
    "series",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), unique=True),
    Column("slug", String(255), unique=True),
    Column("description", Text),
    Column("thumbnail", String(255)),
    Column(
        "created_at",
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    ),
    Column("updated_at", DateTime),
)

series_note_assoc = Table(
    "series_note_assoc",
    metadata,
    Column("series_id", ForeignKey("series.id")),
    Column("note_id", ForeignKey("note.id")),
    UniqueConstraint(
        "series_id",
        "note_id",
        name="series_note_assoc_nq_1",
    ),
)

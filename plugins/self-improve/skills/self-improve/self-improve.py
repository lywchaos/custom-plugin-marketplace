# /// script
# dependencies = ["chromadb", "typer"]
# ///
"""Self-Improve CLI: Store and retrieve strings via semantic search using Chroma."""

import hashlib
from pathlib import Path
from typing import Annotated

import chromadb
import typer

app = typer.Typer(help="Store and retrieve strings via semantic search.")


def find_git_root() -> Path:
    """Walk up from CWD to find .git directory, raise error if not found."""
    current = Path.cwd().resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise typer.Exit(
        code=1,
    )


def get_db_path() -> Path:
    """Return the database path at {git_root}/.claude/self-improve/."""
    git_root = find_git_root()
    db_path = git_root / ".claude" / "self-improve"
    db_path.mkdir(parents=True, exist_ok=True)
    return db_path


def get_collection() -> chromadb.Collection:
    """Initialize Chroma client with persistent storage and get/create collection."""
    db_path = get_db_path()
    client = chromadb.PersistentClient(path=str(db_path))
    return client.get_or_create_collection(
        name="self_improve",
        metadata={"hnsw:space": "cosine"},
    )


def text_to_id(text: str) -> str:
    """Generate a unique ID for a text string using SHA256 hash."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


@app.command()
def add(
    texts: Annotated[
        list[str],
        typer.Argument(help="One or more strings to add to the database."),
    ],
) -> None:
    """Add strings to the database. Skips duplicates silently."""
    try:
        collection = get_collection()
    except typer.Exit:
        typer.echo("Error: Not in a git repository.", err=True)
        raise typer.Exit(code=1)

    for text in texts:
        doc_id = text_to_id(text)
        # Check if document already exists
        existing = collection.get(ids=[doc_id])
        if existing["ids"]:
            # Skip duplicate
            continue
        collection.add(
            documents=[text],
            ids=[doc_id],
        )


@app.command()
def search(
    query: Annotated[str, typer.Argument(help="Query string to search for.")],
    top_k: Annotated[
        int,
        typer.Option("--top-k", "-k", help="Max number of results."),
    ] = 5,
    threshold: Annotated[
        float,
        typer.Option(
            "--threshold", "-t", help="Minimum similarity score (0-1)."
        ),
    ] = 0.5,
) -> None:
    """Search for related strings in the database."""
    try:
        collection = get_collection()
    except typer.Exit:
        typer.echo("Error: Not in a git repository.", err=True)
        raise typer.Exit(code=1)

    # Check if collection is empty
    if collection.count() == 0:
        typer.echo("No results found.")
        return

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
    )

    documents = results["documents"][0] if results["documents"] else []
    # Chroma returns distances for cosine, similarity = 1 - distance
    distances = results["distances"][0] if results["distances"] else []

    found_any = False
    for doc, distance in zip(documents, distances):
        similarity = 1 - distance
        if similarity >= threshold:
            typer.echo(f"[{similarity:.2f}] {doc}")
            found_any = True

    if not found_any:
        typer.echo("No results found.")


if __name__ == "__main__":
    app()

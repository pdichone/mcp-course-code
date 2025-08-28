from datetime import datetime, timezone
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Library Management System", "1.0.0")

# Mock database - In production, this would be a real database
LIBRARY_DATA = {
    "books": [
        {
            "id": "B001",
            "title": "Artificial Intelligence: A Modern Approach",
            "authors": ["Stuart Russell", "Peter Norvig"],
            "isbn": "978-0134610993",
            "category": "Computer Science",
            "publisher": "Pearson",
            "publication_year": 2020,
            "copies_total": 5,
            "copies_available": 2,
            "location": "CS-Section-A-Shelf-12",
            "status": "available",
            "last_updated": "2024-01-15T10:30:00Z",
        },
        {
            "id": "B002",
            "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
            "authors": ["Robert C. Martin"],
            "isbn": "978-0132350884",
            "category": "Software Engineering",
            "publisher": "Prentice Hall",
            "publication_year": 2008,
            "copies_total": 3,
            "copies_available": 0,
            "location": "SE-Section-B-Shelf-05",
            "status": "checked_out",
            "last_updated": "2024-01-20T14:15:00Z",
        },
        {
            "id": "B003",
            "title": "The Design of Everyday Things",
            "authors": ["Donald A. Norman"],
            "isbn": "978-0465050659",
            "category": "Design",
            "publisher": "Basic Books",
            "publication_year": 2013,
            "copies_total": 4,
            "copies_available": 4,
            "location": "DESIGN-Section-C-Shelf-03",
            "status": "available",
            "last_updated": "2024-01-18T09:45:00Z",
        },
        {
            "id": "B004",
            "title": "Database System Concepts",
            "authors": ["Abraham Silberschatz", "Henry Korth", "S. Sudarshan"],
            "isbn": "978-0078022159",
            "category": "Database Systems",
            "publisher": "McGraw-Hill",
            "publication_year": 2019,
            "copies_total": 6,
            "copies_available": 1,
            "location": "DB-Section-A-Shelf-18",
            "status": "available",
            "last_updated": "2024-01-22T16:20:00Z",
        },
    ],
    "members": [
        {
            "id": "M001",
            "name": "Alice Johnson",
            "email": "alice.johnson@university.edu",
            "member_type": "faculty",
            "registration_date": "2023-09-01T00:00:00Z",
            "books_checked_out": ["B002"],
            "max_books": 10,
            "status": "active",
        },
        {
            "id": "M002",
            "name": "Bob Smith",
            "email": "bob.smith@university.edu",
            "member_type": "student",
            "registration_date": "2023-09-15T00:00:00Z",
            "books_checked_out": [],
            "max_books": 5,
            "status": "active",
        },
    ],
    "checkouts": [
        {
            "id": "CO001",
            "book_id": "B002",
            "member_id": "M001",
            "checkout_date": "2024-01-20T14:15:00Z",
            "due_date": "2024-02-20T14:15:00Z",
            "return_date": None,
            "status": "active",
            "renewal_count": 0,
        }
    ],
    "reservations": [
        {
            "id": "R001",
            "book_id": "B002",
            "member_id": "M002",
            "reservation_date": "2024-01-21T10:00:00Z",
            "status": "active",
            "priority": 1,
        }
    ],
}


@mcp.resource("library://catalog")
def get_full_catalog() -> str:
    """
    Returns the complete library catalog with all books and their detailed information.
    """
    try:
        books = LIBRARY_DATA["books"]
        catalog = {
            "total_books": len(books),
            "last_updated": datetime.now().isoformat(),
            "books": books,
        }

        return json.dumps(catalog, indent=2)

    except Exception as e:

        return json.dumps({"error": str(e)})


@mcp.resource("library://available")
def get_available_books() -> str:
    """
    Returns only books that are currently available for checkout.
    """
    try:
        books = LIBRARY_DATA["books"]
        available_books = [book for book in books if book["copies_available"] > 0]

        result = {
            "available_count": len(available_books),
            "total_books": len(books),
            "availability_rate": f"{(len(available_books)/len(books)*100):.1f}%",
            "books": available_books,
        }

        return json.dumps(result, indent=2)

    except Exception as e:

        return json.dumps({"error": str(e)})


@mcp.resource("library://category/{category}")
def get_books_by_category(category: str) -> str:
    """
    Returns books filtered by category (e.g., Computer Science, Design, etc.).
    """
    try:
        books = LIBRARY_DATA["books"]
        filtered_books = [
            book for book in books if book["category"].lower() == category.lower()
        ]

        result = {
            "category": category,
            "book_count": len(filtered_books),
            "books": filtered_books,
        }

        return json.dumps(result, indent=2)

    except Exception as e:

        return json.dumps({"error": str(e)})


@mcp.resource("library://members")
def get_member_information() -> str:
    """
    Returns information about library members and their current checkouts.
    """
    try:
        members = LIBRARY_DATA["members"]
        checkouts = LIBRARY_DATA["checkouts"]
        current_time = datetime.now(timezone.utc)

        # Enhance member data with checkout details
        enhanced_members = []
        for member in members:
            member_copy = member.copy()
            member_books = []

            for checkout in checkouts:
                if (
                    checkout["member_id"] == member["id"]
                    and checkout["status"] == "active"
                ):
                    book = next(
                        (
                            b
                            for b in LIBRARY_DATA["books"]
                            if b["id"] == checkout["book_id"]
                        ),
                        None,
                    )
                    if book:
                        due_date = datetime.fromisoformat(
                            checkout["due_date"].replace("Z", "+00:00")
                        )
                        member_books.append(
                            {
                                "book_title": book["title"],
                                "checkout_date": checkout["checkout_date"],
                                "due_date": checkout["due_date"],
                                "is_overdue": due_date < current_time,
                            }
                        )

            member_copy["current_checkouts"] = member_books
            member_copy["books_checked_out_count"] = len(member_books)
            enhanced_members.append(member_copy)

        result = {
            "total_members": len(members),
            "active_members": len([m for m in members if m["status"] == "active"]),
            "members": enhanced_members,
        }

        return json.dumps(result, indent=2)

    except Exception as e:

        return json.dumps({"error": str(e)})


@mcp.resource("library://overdue")
def get_overdue_books() -> str:
    """
    Returns information about overdue books and members.
    """
    try:
        from datetime import timezone

        checkouts = LIBRARY_DATA["checkouts"]
        # Use timezone-aware current time to match the data format
        current_time = datetime.now(timezone.utc)

        overdue_items = []

        for checkout in checkouts:
            if checkout["status"] == "active":
                due_date = datetime.fromisoformat(
                    checkout["due_date"].replace("Z", "+00:00")
                )
                if due_date < current_time:
                    # Get book and member details
                    book = next(
                        (
                            b
                            for b in LIBRARY_DATA["books"]
                            if b["id"] == checkout["book_id"]
                        ),
                        None,
                    )
                    member = next(
                        (
                            m
                            for m in LIBRARY_DATA["members"]
                            if m["id"] == checkout["member_id"]
                        ),
                        None,
                    )

                    if book and member:
                        days_overdue = (current_time - due_date).days
                        overdue_items.append(
                            {
                                "book_title": book["title"],
                                "book_id": book["id"],
                                "member_name": member["name"],
                                "member_email": member["email"],
                                "checkout_date": checkout["checkout_date"],
                                "due_date": checkout["due_date"],
                                "days_overdue": days_overdue,
                                "fine_amount": days_overdue * 0.50,  # $0.50 per day
                            }
                        )

        result = {
            "overdue_count": len(overdue_items),
            "total_fine_amount": sum(item["fine_amount"] for item in overdue_items),
            "overdue_items": overdue_items,
        }

        return json.dumps(result, indent=2)

    except Exception as e:

        return json.dumps({"error": str(e)})


@mcp.resource("library://stats")
def get_library_statistics() -> str:
    """
    Returns comprehensive library statistics and analytics.
    """
    try:
        books = LIBRARY_DATA["books"]
        members = LIBRARY_DATA["members"]
        checkouts = LIBRARY_DATA["checkouts"]
        reservations = LIBRARY_DATA["reservations"]

        # Calculate statistics
        total_copies = sum(book["copies_total"] for book in books)
        available_copies = sum(book["copies_available"] for book in books)
        checked_out_copies = total_copies - available_copies

        # Category distribution
        categories = {}
        for book in books:
            category = book["category"]
            if category not in categories:
                categories[category] = {"count": 0, "available": 0}
            categories[category]["count"] += 1
            if book["copies_available"] > 0:
                categories[category]["available"] += 1

        # Member type distribution
        member_types = {}
        for member in members:
            member_type = member["member_type"]
            member_types[member_type] = member_types.get(member_type, 0) + 1

        result = {
            "collection_stats": {
                "total_titles": len(books),
                "total_copies": total_copies,
                "available_copies": available_copies,
                "checked_out_copies": checked_out_copies,
                "utilization_rate": f"{(checked_out_copies/total_copies*100):.1f}%",
            },
            "member_stats": {
                "total_members": len(members),
                "active_members": len([m for m in members if m["status"] == "active"]),
                "member_types": member_types,
            },
            "circulation_stats": {
                "active_checkouts": len(
                    [c for c in checkouts if c["status"] == "active"]
                ),
                "active_reservations": len(
                    [r for r in reservations if r["status"] == "active"]
                ),
            },
            "category_breakdown": categories,
            "generated_at": datetime.now().isoformat(),
        }

        return json.dumps(result, indent=2)

    except Exception as e:

        return json.dumps({"error": str(e)})


@mcp.resource("library://category/computer-science")
def get_computer_science_books() -> str:
    """Returns books in Computer Science category."""
    return get_books_by_category("Computer Science")


@mcp.resource("library://category/software-engineering")
def get_software_engineering_books() -> str:
    """Returns books in Software Engineering category."""
    return get_books_by_category("Software Engineering")


@mcp.resource("library://category/database-systems")
def get_database_books() -> str:
    """Returns books in Database Systems category."""
    return get_books_by_category("Database Systems")


if __name__ == "__main__":
    mcp.run()

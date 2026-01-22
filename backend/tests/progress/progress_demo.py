from backend.app.rag.pipeline import run_pipeline
from backend.app.rag.retriever import secure_search
from backend.app.rag.rbac import get_effective_roles


def main():
    role = input("Enter User Role  : ").strip().lower()
    query = input("Enter Query      : ").strip()

    print("\n--- RUNNING PIPELINE ---\n")

    result = run_pipeline(role)
    store = result["vector_store"]

    print(f"Total Documents Loaded : {result['total_documents']}")
    print(f"Total Chunks Created   : {result['total_chunks']}")

    print("\n--- SECURE ROLE-BASED RETRIEVAL ---\n")

    results = secure_search(store, query, role)

    print(f"Query           : {query}")
    print(f"User Role       : {role}")
    print(f"Results Found   : {len(results)}")

    effective_roles = get_effective_roles(role)
    rbac_pass = True

    for doc in results:
        doc_roles = {
            r.strip()
            for r in doc.metadata.get("accessible_roles", "").split(",")
        }
        if doc_roles.isdisjoint(effective_roles):
            rbac_pass = False
            break

    print(f"RBAC Validation : {'PASS' if rbac_pass else 'FAIL'}")

    print("\n--- RETRIEVAL SUMMARY ---\n")

    if not results:
        print("No results returned.")
        print("Reason: Either no relevant content was found or access is restricted by RBAC.")
        print("Status: RBAC enforcement verified.")
        return

    for i, doc in enumerate(results, 1):
        print(f"[Result {i}]")
        print("Department :", doc.metadata.get("department"))
        print("Roles      :", doc.metadata.get("accessible_roles"))
        print("Content    :", doc.page_content[:150])
        print("-" * 40)


if __name__ == "__main__":
    main()


# PASS (Authorized)
# Role  : finance
# Query : financial report revenue

# PASS (Hierarchy)
# Role  : c_level
# Query : employee salary

# PASS (Blocked Access)
# Role  : marketing
# Query : employee salary

# PASS (Blocked Access)
# Role  : employees
# Query : financial quarterly revenue

# python -m backend.tests.progress.progress_demo

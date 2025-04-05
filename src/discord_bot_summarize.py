import requests

# Base URL of your FastAPI app
BASE_URL = "http://127.0.0.1:8000"

# Path to your local PDF file
PDF_PATH = "D:/Programming/Summarize PDF/IRT_Machine_Translation.pdf"

# ---------- Test /full_summarize ----------
def test_full_summarize():
    with open(PDF_PATH, "rb") as f:
        files = {"file": ("IRT_Machine_Translation.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/full_summarize", files=files)

    print("\n✅ Full Summarize Response:")
    print(response.status_code)
    print(response.json())


# ---------- Test /range_summarize ----------
def test_range_summarize(user_input=2):
    with open(PDF_PATH, "rb") as f:
        files = {"file": ("IRT_Machine_Translation.pdf", f, "application/pdf")}
        data = {"user_input": str(user_input)}
        response = requests.post(f"{BASE_URL}/range_summarize", files=files, data=data)

    print("\n✅ Range Summarize Response:")
    print(response.status_code)
    print(response.json())


# Run tests
if __name__ == "__main__":
    test_full_summarize()
    test_range_summarize(user_input=2)

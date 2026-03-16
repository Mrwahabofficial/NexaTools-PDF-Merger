import os
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def clean_path(path):
    # Remove quotes, spaces, newlines
    path = path.strip()
    path = path.strip('"')
    path = path.strip("'")
    path = path.strip()
    return path

def print_header():
    print("=" * 60)
    print("  PDF Merger Pro — NexaTools")
    print("  Merge multiple PDFs into one file")
    print("=" * 60)

def get_pdf_files():
    print("\nOptions:")
    print("  1. Enter PDF file paths manually")
    print("  2. Merge all PDFs from a folder")
    print()
    choice = input("Enter choice (1/2): ").strip()

    files = []

    if choice == "1":
        print("\nHow to add PDF path:")
        print("  - Right click PDF file")
        print("  - Click 'Copy as path'")
        print("  - Paste here with Ctrl+V")
        print("\nPress Enter twice when done.\n")

        while True:
            try:
                raw = input(f"PDF {len(files)+1}: ")
            except EOFError:
                break

            path = clean_path(raw)

            if not path:
                if len(files) >= 2:
                    break
                else:
                    print("  Please enter at least 2 PDF files.")
                    continue

            if not os.path.exists(path):
                print(f"  [ERROR] File not found!")
                print(f"  Tried: {path}")
                print(f"  Tip: Right click file -> Copy as path -> Paste here")
                continue

            if not path.lower().endswith('.pdf'):
                print(f"  [ERROR] Not a PDF file!")
                continue

            files.append(path)
            print(f"  [ADDED] {os.path.basename(path)} ✓")

    elif choice == "2":
        raw = input("\nEnter folder path: ")
        folder = clean_path(raw)

        if not os.path.exists(folder):
            print(f"[ERROR] Folder not found!")
            return []

        files = [
            os.path.join(folder, f)
            for f in sorted(os.listdir(folder))
            if f.lower().endswith('.pdf')
        ]

        if not files:
            print("[ERROR] No PDF files found in folder.")
            return []

        print(f"\nFound {len(files)} PDF files:")
        for f in files:
            print(f"  + {os.path.basename(f)}")

    return files

def merge_pdfs(files, output_path):
    try:
        from pypdf import PdfWriter, PdfReader

        writer = PdfWriter()
        total_pages = 0

        print("\nMerging...")
        for pdf_path in files:
            reader = PdfReader(pdf_path)
            pages = len(reader.pages)
            for page in reader.pages:
                writer.add_page(page)
            total_pages += pages
            print(f"  [MERGED] {os.path.basename(pdf_path)} ({pages} pages)")

        with open(output_path, 'wb') as f:
            writer.write(f)

        return total_pages

    except ImportError:
        print("\n[ERROR] pypdf not installed!")
        print("Run: pip install pypdf")
        return 0

def main():
    clear()
    print_header()

    # Auto install
    try:
        import pypdf
    except ImportError:
        print("\n[SETUP] Installing required library...")
        os.system(f"{sys.executable} -m pip install pypdf -q")
        print("[DONE] Library installed!\n")

    files = get_pdf_files()

    if len(files) < 2:
        print("\n[ERROR] Need at least 2 PDF files to merge.")
        input("\nPress Enter to exit...")
        return

    print(f"\nTotal files: {len(files)}")

    # Output file name
    default_output = "merged_output.pdf"
    output = input(f"\nOutput filename [{default_output}]: ").strip()
    if not output:
        output = default_output
    if not output.endswith('.pdf'):
        output += '.pdf'

    # Preview
    print("\n" + "-" * 60)
    print("Files to merge:")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {os.path.basename(f)}")
    print(f"\nOutput: {output}")
    print("-" * 60)

    confirm = input("\nProceed? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return

    total_pages = merge_pdfs(files, output)

    if total_pages:
        print("\n" + "=" * 60)
        print("  Merge Complete!")
        print(f"  Files merged  : {len(files)}")
        print(f"  Total pages   : {total_pages}")
        print(f"  Output file   : {output}")
        print("=" * 60)

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()

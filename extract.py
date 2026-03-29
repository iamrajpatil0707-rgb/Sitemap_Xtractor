import gzip
import xml.etree.ElementTree as ET
import argparse
import os
import requests
from io import BytesIO
import sys


def fetch_from_url(url):
    print(f"\n[1/3] Downloading sitemap...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/xml, text/xml, application/gzip, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    response = requests.get(url, headers=headers, timeout=60, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    chunks = []
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            chunks.append(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                sys.stdout.write(f"\r    Downloading: {percent:.1f}% ({downloaded//1024} KB / {total_size//1024} KB)")
                sys.stdout.flush()
    
    sys.stdout.write("\n")
    return b''.join(chunks)


def extract_sitemap(source, output_file=None, show_all=True, is_url=False):
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9',
          'xhtml': 'http://www.w3.org/1999/xhtml'}

    try:
        if is_url:
            print(f"[2/3] Processing sitemap...")
            content_bytes = fetch_from_url(source)
            sys.stdout.write("    Decompressing...")
            sys.stdout.flush()
            content = gzip.decompress(content_bytes).decode('utf-8')
            print("    Done!")
        else:
            with gzip.open(source, 'rt', encoding='utf-8') as f:
                content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    try:
        root = ET.fromstring(content)
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return

    urls_data = []

    def find_all(element, path, namespace=None):
        result = element.findall(path, namespace)
        if not result:
            result = element.findall(path.replace('sm:', '').replace('xhtml:', ''))
        return result

    def find_one(element, path, namespace=None):
        result = element.find(path, namespace)
        if result is None:
            result = element.find(path.replace('sm:', '').replace('xhtml:', ''))
        return result

    print("[3/3] Extracting URLs...")
    
    all_urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    if not all_urls:
        all_urls = root.findall('.//url')
    
    total = len(all_urls)
    print(f"    Total URLs found in XML: {total}")
    
    for idx, url in enumerate(all_urls, 1):
        if url is None or url == False:
            continue
            
        loc_elem = find_one(url, 'sm:loc', ns)
        if loc_elem is None:
            loc_elem = url.find('loc')
        loc = loc_elem.text if loc_elem is not None and loc_elem.text else ''
        
        lastmod = ''
        priority = ''
        changefreq = ''
        alternatives = []

        lastmod_elem = find_one(url, 'sm:lastmod', ns)
        if lastmod_elem is None:
            lastmod_elem = url.find('lastmod')
        if lastmod_elem is not None:
            lastmod = lastmod_elem.text or ''

        priority_elem = find_one(url, 'sm:priority', ns)
        if priority_elem is None:
            priority_elem = url.find('priority')
        if priority_elem is not None:
            priority = priority_elem.text or ''

        changefreq_elem = find_one(url, 'sm:changefreq', ns)
        if changefreq_elem is None:
            changefreq_elem = url.find('changefreq')
        if changefreq_elem is not None:
            changefreq = changefreq_elem.text or ''

        for alt in url.findall('.//{http://www.w3.org/1999/xhtml}link'):
            if alt.get('rel') == 'alternate':
                hreflang = alt.get('hreflang', '')
                href = alt.get('href', '')
                alternatives.append(f"{hreflang}: {href}")

        urls_data.append({
            'loc': loc,
            'lastmod': lastmod,
            'priority': priority,
            'changefreq': changefreq,
            'alternatives': alternatives
        })
        
        if idx % 5000 == 0:
            print(f"    Processed: {idx}/{total} URLs...")

    print(f"    Extraction complete! Total: {len(urls_data)} URLs")

    if output_file:
        print(f"\nSaving to file: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in urls_data:
                f.write("=" * 80 + "\n")
                for key, value in item.items():
                    if key == 'alternatives' and value:
                        f.write(f"{key}: {', '.join(value)}\n")
                    else:
                        f.write(f"{key}: {value}\n")
                f.write("\n")
        print(f"[OK] Results saved to: {output_file}")
        print(f"[OK] Total URLs saved: {len(urls_data)}")
    else:
        print(f"\n{'='*80}")
        print(f"Total URLs found: {len(urls_data)}")
        print(f"{'='*80}\n")
        
        for i, item in enumerate(urls_data, 1):
            print(f"#{i}")
            for key, value in item.items():
                if key == 'alternatives' and value:
                    print(f"  {key}: {', '.join(value)}")
                else:
                    print(f"  {key}: {value}")
            print()


def main():
    parser = argparse.ArgumentParser(description='Extract data from sitemap.xml.gz files')
    parser.add_argument('input', help='Path to sitemap.xml.gz file OR URL')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all details')

    args = parser.parse_args()

    is_url = args.input.startswith('http://') or args.input.startswith('https://')

    if not is_url and not os.path.exists(args.input):
        print(f"File not found: {args.input}")
        return

    extract_sitemap(args.input, args.output, args.verbose, is_url)


if __name__ == '__main__':
    main()

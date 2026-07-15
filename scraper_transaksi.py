from playwright.sync_api import sync_playwright
import os
import time



def cek_login(page):

    try:

        url = page.url.lower()


        if "login" in url:
            return True


        if page.locator(
            "input[type='password']"
        ).count() > 0:

            return True


    except:

        pass


    return False





def login_satu_kali(page, site, url):


    if cek_login(page):

        print("====================")
        print("LOGIN MANUAL")
        print("SITE :", site)
        print("====================")


        input(
            "Login selesai tekan ENTER..."
        )


        print(
            "LOGIN BERHASIL"
        )


        page.goto(

            url,

            timeout=60000,

            wait_until="networkidle"

        )


    else:

        print(
            "SESSION SUDAH LOGIN"
        )







def isi_tanggal(

    page,

    start_date,

    end_date

):


    page.evaluate(

        """

        (data)=>{


            let start =
            document.querySelector("#startTime");


            let end =
            document.querySelector("#endTime");



            if(start){

                start.removeAttribute("readonly");

                start.value=data.start;


                start.dispatchEvent(
                    new Event(
                        "change",
                        {
                            bubbles:true
                        }
                    )
                );

            }



            if(end){

                end.removeAttribute("readonly");

                end.value=data.end;


                end.dispatchEvent(
                    new Event(
                        "change",
                        {
                            bubbles:true
                        }
                    )
                );

            }


        }

        """,

        {
            "start": start_date,
            "end": end_date
        }

    )







def ambil_text_tabel(page):

    try:

        return page.locator(
            ".complete-transaction-table"
        ).inner_text()


    except:

        return ""







def tunggu_hasil(page, text_lama):

    try:

        page.wait_for_function(

            """

            (oldText)=>{


                let table =
                document.querySelector(
                    ".complete-transaction-table"
                );


                if(!table)

                    return false;



                let now =
                table.innerText.trim();



                return now !== oldText.trim()
                &&
                now.length > 10;


            }

            """,

            arg=text_lama,

            timeout=30000

        )


        # beri waktu render akhir

        page.wait_for_timeout(1000)


    except Exception as e:

        print(
            "WAIT ERROR:",
            e
        )

def ambil_transaksi(

    site,

    url,

    userids,

    start_date,

    end_date,

    category

):


    profile = (

        "browser_profile/"

        + site

    )



    folder = (

        "screenshots/"

        + site

        + "/TransaksiLengkap"

    )



    os.makedirs(

        folder,

        exist_ok=True

    )







    with sync_playwright() as p:



        context = p.chromium.launch_persistent_context(

            profile,

            headless=False,

            viewport={

                "width":1920,

                "height":1080

            }

        )



        page = context.new_page()





        # =====================
        # BUKA HALAMAN SEKALI
        # =====================


        print(
            "BUKA TRANSAKSI"
        )



        page.goto(

            url,

            timeout=60000,

            wait_until="networkidle"

        )



        page.wait_for_timeout(3000)





        # =====================
        # LOGIN SEKALI
        # =====================


        login_satu_kali(

            page,

            site,

            url

        )





        page.wait_for_selector(

            "#startTime",

            timeout=30000

        )





        # =====================
        # SETTING SEKALI
        # =====================


        isi_tanggal(

            page,

            start_date,

            end_date

        )


        print(
            "TANGGAL OK"
        )





        page.select_option(

            "#gameCategory",

            category

        )


        print(
            "CATEGORY OK"
        )








        # =====================
        # LOOP USER
        # =====================
        # nomor dipakai untuk
        # JUARA 1, JUARA 2 dst
        # =====================


        for nomor, userid in enumerate(

            userids,

            start=1

        ):



            print("================")
            print(
                "JUARA",
                nomor,
                "-",
                userid
            )
            print("================")



            try:



                # simpan kondisi tabel lama

                tabel_lama = ambil_text_tabel(page)





                # isi userid baru

                page.fill(

                    "input[name='userId']",

                    userid

                )


                print(
                    "USER OK"
                )





                # submit

                page.click(

                    "a.jq-submit-button"

                )


                print(
                    "SUBMIT"
                )





                # tunggu hasil berubah

                tunggu_hasil(

                    page,

                    tabel_lama

                )


                print(
                    "DATA SELESAI LOAD"
                )





                # tunggu render terakhir

                page.wait_for_timeout(1000)





                # =====================
                # CARI AREA SCREENSHOT
                # =====================


                title = page.locator(

                    ".search-title",

                    has_text="Transaksi Lengkap"

                )



                if title.count() == 0:


                    print(
                        "Judul tidak ditemukan"
                    )


                    continue





                box = title.first

                for i in range(10):


                    parent = box.locator(
                        ".."
                    )



                    if parent.locator(

                        ".complete-transaction-table"

                    ).count() > 0:



                        box = parent

                        break



                    box = parent





                # =====================
                # NAMA FILE JUARA
                # =====================


                filename = (

                    folder

                    + "/JUARA "

                    + str(nomor)

                    + ".png"

                )





                box.screenshot(

                    path=filename

                )





                print(
                    "SS SELESAI :",
                    filename
                )





                # =====================
                # KOSONGKAN USER
                # =====================


                page.fill(

                    "input[name='userId']",

                    ""

                )





            except Exception as e:



                print(

                    "ERROR",

                    userid,

                    e

                )







        context.close()



        print("================")
        print("SEMUA SELESAI")
        print("================")
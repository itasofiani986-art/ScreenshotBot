from playwright.sync_api import sync_playwright
from blur import blur_image_text
from sensor_list import SENSOR_TETAP

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







def tunggu_login(page, site, url):


    if cek_login(page):


        print("======================")
        print("LOGIN MANUAL")
        print("SITUS :", site)
        print("Silakan login")
        print("Tekan ENTER jika selesai")
        print("======================")


        input()


        print(
            "LOGIN BERHASIL"
        )


        page.goto(

            url,

            timeout=60000,

            wait_until="domcontentloaded"

        )






def tambah_box_blur(

    daftar,

    posisi,

    box_position

):


    if posisi and box_position:


        posisi_fix = {

            "x":
            posisi["x"] - box_position["x"],


            "y":
            posisi["y"] - box_position["y"],


            "width":
            posisi["width"],


            "height":
            posisi["height"]

        }


        print(
            "POSISI BLUR:",
            posisi_fix
        )


        daftar.append(
            posisi_fix
        )







def tunggu_tabel(page):


    try:

        page.wait_for_selector(

            ".table-title",

            timeout=15000

        )


        page.wait_for_selector(

            "th",

            timeout=15000

        )


        page.wait_for_timeout(300)



    except:


        pass

def ambil_semua(

    site,

    base_url,

    userkeys,

    sensor_words=None

):


    profile = (

        f"browser_profile/{site}"

    )



    folder = (

        "screenshots/"

        +

        site

        +

        "/HistoryCoin"

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



        page = (

            context.pages[0]

            if context.pages

            else context.new_page()

        )







        for nomor, userkey in enumerate(

            userkeys,

            start=1

        ):



            print("================")
            print(
                "JUARA",
                nomor,
                "-",
                userkey
            )
            print("================")



            url = base_url + userkey



            try:



                page.goto(

                    url,

                    timeout=60000,

                    wait_until="domcontentloaded"

                )





                tunggu_tabel(page)





                tunggu_login(

                    page,

                    site,

                    url

                )






                title = page.locator(

                    ".table-title",

                    has_text="History Coin"

                )





                if title.count() == 0:


                    print(

                        "History Coin tidak ditemukan"

                    )


                    continue






                box = title.first.locator(

                    ".."

                )



                box_position = box.bounding_box()





                if not box_position:


                    print(

                        "BOX TIDAK ADA"

                    )


                    continue






                # ==========================
                # HAPUS ROW SETELAH DATA 1
                # ==========================


                page.evaluate(

                """

                () => {


                    let rows =
                    document.querySelectorAll(
                        "tr,.table-row,.row"
                    );


                    let mulai=false;



                    rows.forEach(row=>{


                        let text =
                        row.innerText.trim();



                        if(

                            text.startsWith("1")

                            &&

                            !mulai

                        ){

                            mulai=true;

                            return;

                        }



                        if(mulai){

                            row.style.display="none";

                        }


                    });


                }

                """

                )





                sensor_boxes=[]





                # ==========================
                # SENSOR ID
                # ==========================


                target_id = box.locator(

                    f"text={userkey}"

                )



                if target_id.count() > 0:


                    posisi = target_id.first.bounding_box()



                    if posisi:


                        tambah_box_blur(

                            sensor_boxes,

                            posisi,

                            box_position

                        )

                # ==========================
                # SENSOR TAMBAHAN
                # ==========================


                semua_sensor = list(SENSOR_TETAP)



                if sensor_words:


                    semua_sensor.extend(

                        sensor_words

                    )



                semua_sensor = list(set(

                    semua_sensor

                ))





                print(
                    "CEK SENSOR:",
                    semua_sensor
                )





                for kata in semua_sensor:



                    if kata == userkey:

                        continue



                    try:


                        target = box.locator(

                            f"text={kata}"

                        )



                        if target.count() > 0:



                            posisi = target.first.bounding_box()



                            if posisi:


                                tambah_box_blur(

                                    sensor_boxes,

                                    posisi,

                                    box_position

                                )



                    except Exception as e:


                        print(

                            "ERROR SENSOR",

                            kata,

                            e

                        )







                # ==========================
                # SCREENSHOT TANPA LAST COIN
                # ==========================


                file = (

                    folder

                    + "/JUARA "

                    + str(nomor)

                    + ".png"

                )





                bbox = box.bounding_box()





                if bbox:



                    last = box.locator(

                        "th",

                        has_text="Last Coin"

                    )



                    if last.count() > 0:



                        lastbox = last.first.bounding_box()



                        if lastbox:



                            clip = {


                                "x":

                                bbox["x"],



                                "y":

                                bbox["y"],



                                "width":

                                lastbox["x"] - bbox["x"],



                                "height":

                                bbox["height"]


                            }



                            page.screenshot(

                                path=file,

                                clip=clip

                            )



                        else:


                            box.screenshot(

                                path=file

                            )


                    else:


                        box.screenshot(

                            path=file

                        )



                else:


                    box.screenshot(

                        path=file

                    )







                # ==========================
                # BLUR
                # ==========================


                blur_image_text(

                    file,

                    sensor_boxes

                )





                print(

                    "SUKSES:",

                    file

                )







            except Exception as e:


                print(

                    "ERROR",

                    site,

                    userkey,

                    e

                )








        context.close()



        print("================")
        print("SELESAI")
        print("================")
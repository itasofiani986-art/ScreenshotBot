from flask import Flask, render_template, request, send_from_directory
import os

from scraper import ambil_semua
from scraper_transaksi import ambil_transaksi


app = Flask(__name__)


SCREENSHOT_FOLDER = "screenshots"


LAST_RESULT = []



SITES = {

    "WDBOS":
    "https://agent.png777.com/player-knowledge.html?userkey=",


    "DEPOBOS":
    "https://depobos.idrbo1.com/player-knowledge.html?userkey=",


    "LATOTO":
    "https://ag-latoto.idrbo.com/player-knowledge.html?userkey=",


    "ANGKABET":
    "https://angkabet.idrbo1.com/player-knowledge.html?userkey=",


    "PULITOTO":
    "https://pulitoto.idrbo1.com/player-knowledge.html?userkey="

}





TRANSAKSI = {

    "WDBOS":
    "https://agent.png777.com/complete-transaction.html",


    "DEPOBOS":
    "https://depobos.idrbo1.com/complete-transaction.html",


    "LATOTO":
    "https://ag-latoto.idrbo.com/complete-transaction.html",


    "ANGKABET":
    "https://angkabet.idrbo1.com/complete-transaction.html",


    "PULITOTO":
    "https://pulitoto.idrbo1.com/complete-transaction.html"

}







@app.route("/")
def index():

    return render_template(

        "index.html",

        sites=SITES.keys(),

        files=LAST_RESULT

    )









@app.route(
    "/proses",
    methods=["POST"]
)
def proses():


    global LAST_RESULT


    LAST_RESULT.clear()



    mode = request.form.get(
        "mode"
    )


    site = request.form.get(
        "site"
    )


    ids = request.form.get(
        "ids",
        ""
    )



    sensor = request.form.get(
        "sensor",
        ""
    )



    sensor_words = []



    for x in sensor.splitlines():


        x = x.strip()


        if x:

            sensor_words.append(x)







    userids = []



    for x in ids.splitlines():


        x = x.strip()


        if x:

            userids.append(x)







    if not userids:


        return """

        <script>

        alert('ID kosong');

        history.back();

        </script>

        """









    # ==========================
    # HISTORY COIN
    # ==========================


    if mode == "history":



        ambil_semua(

            site,

            SITES[site],

            userids,

            sensor_words

        )



        folder = (

            "screenshots/"

            +

            site

            +

            "/HistoryCoin"

        )









    # ==========================
    # TRANSAKSI
    # ==========================


    else:



        ambil_transaksi(

            site,

            TRANSAKSI[site],

            userids,

            request.form.get(
                "start"
            ),

            request.form.get(
                "end"
            ),

            request.form.get(
                "category"
            )

        )



        folder = (

            "screenshots/"

            +

            site

            +

            "/TransaksiLengkap"

        )









    # ==========================
    # HASIL SCREENSHOT
    # ==========================


    for userid in userids:



        file_path = (

            folder

            +

            "/"

            +

            userid

            +

            ".png"

        )



        if os.path.exists(file_path):



            link_file = file_path.replace(

                "\\",

                "/"

            )



            if link_file.startswith(
                "screenshots/"
            ):


                link_file = link_file[

                    len("screenshots/")

                ]



            LAST_RESULT.append(

                link_file

            )







    return """

    <script>

    alert(
        'Screenshot selesai'
    );


    location.href='/';


    </script>

    """









@app.route(
    "/screenshots/<path:filename>"
)
def screenshot(filename):


    return send_from_directory(

        SCREENSHOT_FOLDER,

        filename

    )











if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )
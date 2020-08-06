
console.log("moo")

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );

    var http = new XMLHttpRequest();
    var url = 'test';
    var params = 'foo=Woo&bar=3';
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            alert(http.responseText);
        }
    }
http.send(params);

    return xmlHttp.responseText;
}

msg = httpGet("http://127.0.0.1:5000/me")
console.log(msg)

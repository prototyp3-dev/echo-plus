# echo-plus DApp

```
Cartesi Rollups version: 1.0.x
```

echo-plus is a customized DApp written in Python, which originally resembles the one provided by the sample [Echo Python DApp](https://github.com/cartesi/rollups-examples/tree/main/echo-python).
Contrary to that example, this DApp uses sunodo to build and run, and as such the commands for building, and running are different.

## Requirements

This project works with [sunodo](https://github.com/sunodo/sunodo), so run it you should first install sunodo.

```shell
npm install -g @sunodo/cli
alias sunodo="npx @sunodo/cli"
```

## Building

To build the application, run the following command:

```shell
sunodo build
```

## Running

To start the application, execute the following command:

```shell
sunodo run
```

The application can afterwards be shut down with ctrl+c

## Interacting with the application

You can send using ```sunodo send``` command. Optionally, you can use the frontend web [frontend-web](https://github.com/prototyp3-dev/frontend-web-cartesi) application to interact with the DApp. 

The DApp works as an echo dapp, but it answers some special commands such as:
1. deposits (it sends vouchers to depositor with the same assets)
2. json 
    You can check if lat long lies within a fence - e.g.: 
    
    ```{"latitude":34.639,"longitude":-118.051,"fence":"{\"type\":\"Polygon\",\"coordinates\":[[[-118.053,34.6403],[-118.050492679131423,34.637611825591407],[-118.04191282470596,34.642500320185789],[-118.044382904834507,34.645229032100403],[-118.053002827442867,34.640396678176792]]]}"}```
    
    You can send sql statements - e.g.: 
    
    ```{"sql":"create table developers (name string, company string, age integer);"}```
    
    ```{"sql":"insert into developers (name, company, age) values('John', 'abc company', 50);"}```
    
    ```{"sql":"select * from developers;"}```
    
    You can send arrays to be ordered with numpy - e.g.: 
    
    ```{"array":[3,5,1,4,2]}```

    You can send mint nfts - e.g.: 
    
    ```{"erc721_to_mint":"0xd8b9...3fa8","selector":"0x755edd17"}```

    ```{"erc721_to_mint":"0xd914...9138","selector":"0xd0def521","string":"nftTest"}```

    You can send images (converted to base64) to be processed with opencv (and mint nft with file multihash) - e.g.: 
    
    ```{"image":"iVBORw0...uQmCC"}```

    ```{"image":"iVBORw0...uQmCC","erc721_to_mint":"0xd914...9138","selector":"0xd0def521"}```

    Using standard linux tools you can convert an image to base64 with ```base64 img.png``` and convert back to with ```base64 -d <<< $(cat img_processed.png.b64) > img_processed.png```

3. strings (it performs some operations depending on the string: report, reject, exception, ...)


## Running the back-end in host mode

When developing an application, it is often important to easily test and debug it. For that matter, it is possible to run the Cartesi Rollups environment with the backend running in the host machine, allowing it to be debugged using regular development tools such as an IDE.

To start the rollups node, execute the following command:

```
sunodo run --no-backend
```

This DApp's back-end is written in Python, so to run it in your machine you need to have `python3` installed.
The backend uses shapely library, so you should install libgeos-c on your host (refer to [geos](https://libgeos.org/usage/install/)).

In order to start the back-end, run the following commands in a dedicated terminal:

```shell
cd dapp
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-host.txt
ROLLUP_HTTP_SERVER_URL="http://localhost:8080/host-runner" python3 echo-plus.py
```

# 第 6 章 Hello World メモ

## この章の目的

- Arduinoへのデプロイ方法を学習

## キーアイデア

- （読み進めながら箇条書きで）

## やってみたこと

- [x] Arduino Nano 33 BLE SenseとIDEの準備
- [x] deployと動作確認
  - src/deployment/hello_wqorld

## 疑問・メモ

- 疑問:
- メモ:
  - PowerShellの管理者でusbipdをインストール
```
# 1) GitHub API から最新版 release 情報を取得し、x64/amd64 MSI を選んでダウンロード->検証->イン ストール
>> $headers = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT)' }
>>
>> # get release info
>> $release = Invoke-RestMethod -Uri 'https://api.github.com/repos/dorssel/usbipd-win/releases/latest' -Headers $headers
>>
>> # list assets (optional visual check)
>> $release.assets | Select-Object name, browser_download_url
>>
>> # pick asset containing x64/amd64 (if none, we'll show the list above)
>> $asset = $release.assets | Where-Object { $_.name -match 'x64|amd64' } | Select-Object -First 1
>> if (-not $asset) {
>>   Write-Output "x64/amd64 asset not found. Paste the asset list above in your reply."
>>   exit 1
>> }
>>
>> Write-Output "Downloading: $($asset.browser_download_url)"
>> # download (follows redirects)
>> Invoke-WebRequest -Uri $asset.browser_download_url -OutFile "$env:TEMP\usbipd-win.msi" -Headers $headers -UseBasicParsing
>>
>> # show file size
>> Get-Item "$env:TEMP\usbipd-win.msi" | Select-Object Name, Length
>>
>> # show first 4 bytes in hex (MSI usually starts with D0 CF 11 E0)
>> $bytes = [System.IO.File]::ReadAllBytes("$env:TEMP\usbipd-win.msi")
>> ($bytes[0..3] | ForEach-Object { "{0:X2}" -f $_ }) -join ' '
>>
>> # If the file looks good (Length > 100000 and header D0 CF 11 E0), install:
>> Start-Process msiexec.exe -Wait -ArgumentList "/i `"$env:TEMP\usbipd-win.msi`""
>>
>> # Verify installation
>> usbipd --version
>>
>> # List USB devices for WSL attach (note the 'busid' column)
>> usbipd wsl list
```

  - PowerShellでUSBをwslにアタッチ
```shell
> usbipd list
3-1    2341:805a  USB シリアル デバイス (COM4)                                 Not Shared
```
# 上のリストでは3-1がcom4に充てられている
```
usbipd bind --busid 3-1
usbipd attach --busid 3-1 --wsl Ubuntu-24.04
usbipd list
>> wsl -l -v
```

  - wslにarduino-cliをインストール
```
$ curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
$ echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
$ source ~/.bashrc
```
  - wslにコア/ボードをインストール
```
$ arduino-cli core update-index
$ arduino-cli core install arduino:mbed_nano
```
  - wslでコンパイル＆アップロード
```
$ arduino-cli compile --fqbn arduino:mbed_nano:nano33ble ~/work/Oreilly_TinyML/src/deployment/hello_world -v
$ arduino-cli upload --fqbn arduino:mbed_nano:nano33ble -p /dev/ttyACM0 ~/work/Oreilly_TinyML/src/deployment/hello_world
```

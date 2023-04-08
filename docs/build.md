## Build it yourself
Clone the repository:
```
git clone https://github.com/Acumane/commitment.git
cd commitment
```
Install dependencies:
```
pip install pyinstaller rich requests
```
Build & run executable on:
### Linux
<details>
  <summary>Make "commitment"</summary>

 ```
pyinstaller -F main.py -n commitment
cd dist
./commitment
```
</details>


### Windows

<details>
  <summary>Make "commitment.exe"</summary>

```
pyinstaller -c -F main.py -n commitment -i icon.ico
cd dist
commitment.exe
```
</details>

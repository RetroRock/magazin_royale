## Backup for ZDF Magazin Royale content

[Link to show](https://www.zdf.de/comedy/zdf-magazin-royale)

![ZDF Magazin Royale Hero Image](https://www.zdf.de/assets/sb-zdf-magazin-royale-buehne-100~1152x1296?cb=1649762937132 "Jan")

Create automatic backups for your favorite shows using **[youtube-dl](https://youtube-dl.org/)** and **[webdav](https://github.com/ezhov-evgeny/webdav-client-python-3)**. This should also work for every website, **youtube-dl** supports.

### How to run

Add a `.env` file to your working directory. You can find an example [here](https://github.com/RetroRock/magazin_royale/blob/master/.env.md)

Run the [container image](https://hub.docker.com/repository/docker/retrorock/zdf-magazin-royale):

```
docker pull retrorock/zdf-magazin-royale
docker-compose up
```

Enjoy! 🍿

# PoultryBase - Docker Commands

This project uses Docker and Docker Compose to manage a CLI-based chicken record system and its MySQL database. Below are the most useful commands to help you run, manage, and debug the application.

---

## 🚀 Starting and Stopping the Application

 **Start all containers and stream logs:** 

```bash
docker-compose up
```

 **Start containers in the background:** 

```bash
docker-compose up -d
```

 **Stop and remove all containers, volumes, and networks:** 

```bash
docker-compose down
```

 **Restart all services:** 

```bash
docker-compose restart
```

---

## 🛠️ Building Containers

 **Build images (or rebuild if needed):** 

```bash
docker-compose build
```

 **Build and start everything in one command:** 

```bash
docker-compose up --build
```

---

## 📋 Logs and Status

 **View logs for all services:** 

```bash
docker-compose logs
```

 **Follow logs live (like tail -f):** 

```bash
docker-compose logs -f
```

 **Check container status:** 

```bash
docker-compose ps
```

---

## 🐚 Working Inside Containers

 **Access a shell inside the app container:** 

```bash
docker-compose exec app bash
```

 **Open MySQL client inside the db container:** 

```bash
docker-compose exec db mysql -uroot -p
```

---

## 🧪 Running App Once Interactively

 **Run the app container interactively and auto-remove when done:** 

```bash
docker-compose run --rm app
```

---

## 🌐 Access phpMyAdmin (Optional)

If you’ve set up phpMyAdmin in your `docker-compose.yml` :

 **Visit in your browser:** 

```
http://localhost:8080
```

 **Login credentials:** 
* **Username:** root
* **Password:** root
* **Server:** db

---

## ✅ Need Help?

Feel free to ask for help or open an issue if something doesn't work!

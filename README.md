# easytopics

This is a web application to preprocess textual data with LLMs, cluster the results and visualize them. WIP.

# Backend

Make sure to expose environment variables as stated in `backend/.envrc_template`.

# Built with:

- [Node.js](https://nodejs.org/en) 20.5.1
- [yarn](https://yarnpkg.com/) 1.22.19
- [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/) 3.3.3
- [Python](https://www.python.org/) 3.10.13

# Run development version

 Assert you have Python 3.10 installed, as well as Node.js and yarn.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Do not forget to expose environment variables as stated in `backend/.envrc_template`.

Next we install the frontend dependencies:

```bash
cd frontend
yarn install
```

To run the backend exposed at localhost:5000, the clear flag is optional and removes the demo database. This takes a while at startup.

```bash
cd ../backend
bash start_backend.sh --clear
```

To run the frontend exposed at localhost:5173:

```bash
cd ../frontend
yarn dev
```

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Acknowledgments
Icon cat-curled by [svgrepo](https://www.svgrepo.com/svg/452950/cat-curled).
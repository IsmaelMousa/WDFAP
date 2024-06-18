## Installation Guide for WDFAP

To set up and start using **WDFAP**, please follow these detailed instructions:

1. **Clone the Repository**

```zsh
git clone git@github.com:IsmaelMousa/WDFAP.git
```

2. **Navigate to the WDFAP directory**

```zsh
cd WDFAP
```

3. **Setup The Virtual Environment**

```zsh
python3 -m venv .venv
```

4. **Activate The Virtual Environment**

```zsh
# Linux/MacOS 
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

5. **Setup WDFAP**

```zsh
make setup
```

---

### Additional Information

- **Prerequisites:**
    - Ensure that you have git installed on your machine. You can check this by running `git --version`.
    - Verify that **Python 3.10** or higher is installed. Check this with `python3 --version`.


- **Deactivating the Virtual Environment:**

    - When you are done working in the virtual environment, you can deactivate it by simply running:
      ```Bash
      deactivate
      ```

- **Updating WDFAP:**

    - To update WDFAP to the latest version, navigate to the WDFAP directory and pull the latest changes:
        ```Bash
        git pull origin main
        ```

<br> 



By following these instructions, you should be able to set up and start using WDFAP without any issues. If you need
further assistance, please refer to the project's documentation or contact the maintainers.

---

<div align="right">

**[Go Back ➡️](index.md)**

</div>
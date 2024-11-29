/*document.addEventListener("DOMContentLoaded", () => {
    const salesTableBody = document.getElementById("salesTableBody");
    const noProductMessage = document.getElementById("noProductMessage");
    const quantityInput = document.getElementById("quantityInput");
    const resetButton = document.getElementById("quantityButton");
    const cancelButton = document.getElementById("cncl");
    const subtotalDisplay = document.getElementById("subtotalDisplay");
    const productRows = document.querySelectorAll(".product-row");

    // Function to load products from localStorage and update the table
    function loadProductsFromLocalStorage() {
        const products = JSON.parse(localStorage.getItem("selectedProducts") || "[]");

        salesTableBody.innerHTML = "";

        if (products.length > 0) {
            noProductMessage.style.display = "none";

            products.forEach(product => {
                const newRow = document.createElement("tr");
                newRow.dataset.barcode = product.barcode; // Attach barcode for identification
                newRow.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.barcode}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                    <td class="product-quantity">${product.quantity}</td>
                `;
                salesTableBody.appendChild(newRow);
            });
        } else {
            noProductMessage.style.display = "block";
        }
    }

    // Load products when the page loads
    loadProductsFromLocalStorage();

    // Event listener for product row clicks
    productRows.forEach(row => {
        row.addEventListener("click", () => {
            const barcode = row.dataset.barcode;
            const name = row.dataset.name;
            const description = row.dataset.description;
            const price = parseFloat(row.dataset.price);
            const quantityToAdd = parseInt(quantityInput.value || "1");

            if (quantityToAdd < 1) {
                alert("Quantity must be at least 1.");
                return;
            }

            noProductMessage.style.display = "none";

            const existingRow = [...salesTableBody.rows].find(r => r.dataset.barcode === barcode);

            if (existingRow) {
                const currentQuantity = parseInt(existingRow.querySelector(".product-quantity").textContent);
                const newQuantity = currentQuantity + quantityToAdd;

                existingRow.querySelector(".product-quantity").textContent = newQuantity;

                const selectedProducts = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
                const productToUpdate = selectedProducts.find(product => product.barcode === barcode);
                if (productToUpdate) productToUpdate.quantity = newQuantity;
                localStorage.setItem("selectedProducts", JSON.stringify(selectedProducts));
            } else {
                const newRow = document.createElement("tr");
                newRow.dataset.barcode = barcode;
                newRow.innerHTML = `
                    <td>${name}</td>
                    <td>${barcode}</td>
                    <td>${description}</td>
                    <td>${price}</td>
                    <td class="product-quantity">${quantityToAdd}</td>
                `;
                salesTableBody.appendChild(newRow);

                const selectedProducts = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
                selectedProducts.push({ barcode, name, description, price, quantity: quantityToAdd });
                localStorage.setItem("selectedProducts", JSON.stringify(selectedProducts));
            }

            quantityInput.value = "";
        });
    });

    // Cancel button logic
    cancelButton.addEventListener("click", () => {
        localStorage.removeItem("selectedProducts");
        salesTableBody.innerHTML = "";
        noProductMessage.style.display = "block";
        subtotalDisplay.innerText = "";
    });

    // Subtotal calculation
    function calculateSubtotal() {
        const products = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
        let subtotal = 0;

        products.forEach(product => {
            subtotal += product.price * product.quantity;
        });

        subtotalDisplay.innerText = `Subtotal: $${subtotal.toFixed(2)}`;
    }

    // Subtotal button logic
    document.getElementById("sbttl").addEventListener("click", calculateSubtotal);

    // Total button logic
    document.getElementById("totl").addEventListener("click", () => {
        const rows = document.querySelectorAll("#salesTableBody tr");
        const selectedProducts = [];

        rows.forEach(row => {
            const barcode = row.dataset.barcode;
            const quantityCell = row.querySelector(".product-quantity");
            const quantity = parseInt(quantityCell?.textContent || "0", 10);

            if (barcode && quantity > 0) {
                selectedProducts.push({ barcode, quantity });
            }
        });

        if (selectedProducts.length > 0) {
            fetch("/update-quantities/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ products: selectedProducts })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Sale completed!");
                    localStorage.removeItem("selectedProducts");
                    loadProductsFromLocalStorage();
                    calculateSubtotal();
                } else {
                    alert("Error: " + data.errors.join(", "));
                }
            })
            .catch(err => {
                alert("An error occurred: " + err);
            });
        } else {
            alert("No products selected!");
        }
    });
});*/

document.addEventListener("DOMContentLoaded", () => {
    const salesTableBody = document.getElementById("salesTableBody");
    const noProductMessage = document.getElementById("noProductMessage");
    const quantityInput = document.getElementById("quantityInput");
    const resetButton = document.getElementById("quantityButton");
    const cancelButton = document.getElementById("cncl");
    const subtotalDisplay = document.getElementById("subtotalDisplay");

    // Function to load products from localStorage and update the table
    function loadProductsFromLocalStorage() {
        const products = JSON.parse(localStorage.getItem("selectedProducts") || "[]");

        salesTableBody.innerHTML = "";

        if (products.length > 0) {
            noProductMessage.style.display = "none";

            products.forEach(product => {
                const newRow = document.createElement("tr");
                newRow.classList.add("product-row");
                newRow.dataset.barcode = product.barcode; // Attach barcode for identification
                newRow.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.barcode}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                    <td class="product-quantity">${product.quantity}</td>
                `;
                salesTableBody.appendChild(newRow);
            });
        } else {
            noProductMessage.style.display = "block";
        }
    }

    // Load products when the page loads
    loadProductsFromLocalStorage();

    // Event listener for dynamically added rows
    document.addEventListener("click", (event) => {
        if (event.target.closest('.product-row')) {
            const row = event.target.closest('.product-row');
            const barcode = row.dataset.barcode;
            const name = row.dataset.name;
            const description = row.dataset.description;
            const price = parseFloat(row.dataset.price);
            const quantityToAdd = parseInt(quantityInput.value || "1");

            if (quantityToAdd < 1) {
                alert("Quantity must be at least 1.");
                return;
            }

            noProductMessage.style.display = "none";
            const existingRow = [...salesTableBody.rows].find(r => r.dataset.barcode === barcode);

            if (existingRow) {
                const currentQuantity = parseInt(existingRow.querySelector(".product-quantity").textContent);
                const newQuantity = currentQuantity + quantityToAdd;

                existingRow.querySelector(".product-quantity").textContent = newQuantity;

                const selectedProducts = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
                const productToUpdate = selectedProducts.find(product => product.barcode === barcode);
                if (productToUpdate) productToUpdate.quantity = newQuantity;
                localStorage.setItem("selectedProducts", JSON.stringify(selectedProducts));
            } else {
                const newRow = document.createElement("tr");
                newRow.classList.add("product-row");
                newRow.dataset.barcode = barcode;
                newRow.innerHTML = `
                    <td>${name}</td>
                    <td>${barcode}</td>
                    <td>${description}</td>
                    <td>${price}</td>
                    <td class="product-quantity">${quantityToAdd}</td>
                `;
                salesTableBody.appendChild(newRow);

                const selectedProducts = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
                selectedProducts.push({ barcode, name, description, price, quantity: quantityToAdd });
                localStorage.setItem("selectedProducts", JSON.stringify(selectedProducts));
            }

            quantityInput.value = "";
        }
    });

    // Cancel button logic
    cancelButton.addEventListener("click", () => {
        localStorage.removeItem("selectedProducts");
        salesTableBody.innerHTML = "";
        noProductMessage.style.display = "block";
        subtotalDisplay.innerText = "";
    });

    // Subtotal calculation
    function calculateSubtotal() {
        const products = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
        let subtotal = 0;

        products.forEach(product => {
            subtotal += product.price * product.quantity;
        });

        subtotalDisplay.innerText = `Subtotal: $${subtotal.toFixed(2)}`;
    }

    // Subtotal button logic
    document.getElementById("sbttl").addEventListener("click", calculateSubtotal);

    // Total button logic
    document.getElementById("totl").addEventListener("click", () => {
        const rows = document.querySelectorAll("#salesTableBody tr");
        const selectedProducts = [];

        rows.forEach(row => {
            const barcode = row.dataset.barcode;
            const quantityCell = row.querySelector(".product-quantity");
            const quantity = parseInt(quantityCell?.textContent || "0", 10);

            if (barcode && quantity > 0) {
                selectedProducts.push({ barcode, quantity });
            }
        });

        if (selectedProducts.length > 0) {
            fetch("/update_quantities/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ products: selectedProducts })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Server returned an error: " + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert("Sale completed!");
                    localStorage.removeItem("selectedProducts");
                    loadProductsFromLocalStorage();
                    calculateSubtotal();
                } else {
                    alert("Error: " + data.errors.join(", "));
                }
            })
            .catch(err => {
                alert("An error occurred: " + err);
            });
        } else {
            alert("No products selected!");
        }
    });
});

// Function to get CSRF token (needed for secure form submissions)
function getCSRFToken() {
    const cookie = document.cookie.split(";").find(c => c.trim().startsWith("csrftoken="));
    return cookie ? cookie.split("=")[1] : "";
}



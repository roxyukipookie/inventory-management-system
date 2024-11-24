document.addEventListener("DOMContentLoaded", () => {
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

        // Clear the table first
        salesTableBody.innerHTML = "";

        if (products.length > 0) {
            // If there are products, hide the "No products selected" message
            noProductMessage.style.display = "none";

            // Add all products from localStorage to the sales table
            products.forEach(product => {
                const newRow = document.createElement("tr");
                newRow.innerHTML = `
                    <td>${product.name}</td>
                    <td>${product.description}</td>
                    <td>${product.price}</td>
                    <td class="product-quantity">${product.quantity}</td>
                `;
                salesTableBody.appendChild(newRow);
            });
        } else {
            // If no products, display the "No products selected" message
            noProductMessage.style.display = "block";
        }
    }

    // Load previously selected products when the page loads
    loadProductsFromLocalStorage();

    // Event listener for product row clicks
    productRows.forEach(row => {
        row.addEventListener("click", () => {
            const name = row.dataset.name;
            const description = row.dataset.description;
            const price = parseFloat(row.dataset.price);
            const quantity = parseInt(quantityInput.value || 1);

            // Hide "No products selected" message when a product is selected
            noProductMessage.style.display = "none";

            // Add the selected product as a new row in the sales terminal table
            const newRow = document.createElement("tr");
            newRow.innerHTML = `
                <td>${name}</td>
                <td>${description}</td>
                <td>${price}</td>
                <td class="product-quantity">${quantity}</td>
            `;
            salesTableBody.appendChild(newRow);

            // Save the selected product to localStorage
            const selectedProducts = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
            selectedProducts.push({ name, description, price, quantity });
            localStorage.setItem("selectedProducts", JSON.stringify(selectedProducts));
        });
    });

    // Reset button logic: clears the input field
    resetButton.addEventListener("click", () => {
        quantityInput.value = ""; // Clear the input field
    });

    // Cancel button logic: clear products from the table and localStorage
    cancelButton.addEventListener("click", () => {
        localStorage.removeItem("selectedProducts"); // Clear products from localStorage
        salesTableBody.innerHTML = ""; // Remove all products from table

        // Show the "No products selected" message after canceling the transaction
        noProductMessage.style.display = "block";

        // Clear the subtotal
        subtotalDisplay.innerText = "";
    });

    // Calculate and display subtotal
    function calculateSubtotal() {
        const products = JSON.parse(localStorage.getItem("selectedProducts") || "[]");
        let subtotal = 0;

        // Loop through selected products and calculate the subtotal
        products.forEach(product => {
            subtotal += product.price * product.quantity; // Price * Quantity
        });

        // Display the subtotal in the appropriate element
        subtotalDisplay.innerText = `Subtotal: $${subtotal.toFixed(2)}`;
    }

    // Subtotal button logic
    document.getElementById("sbttl").addEventListener("click", calculateSubtotal);
});

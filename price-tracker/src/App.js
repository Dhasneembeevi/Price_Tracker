import React, { useState } from "react";
import axios from "axios";

function App() {
  const [productName, setProductName] = useState("");
  const [amazonPrice, setAmazonPrice] = useState("");
  const [flipkartPrice, setFlipkartPrice] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // const response = await axios.post("http://localhost:8000/get-prices", {
      const response = await axios.post(
        "https://price-tracker-mqo8.onrender.com/get-prices",
        {
          product_name: productName,
        }
      );

      setAmazonPrice(response.data.amazon_price);
      setFlipkartPrice(response.data.flipkart_price);
    } catch (error) {
      console.error("Error fetching prices", error);
      alert("Failed to get prices. Make sure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>🛒 Price Comparison</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          placeholder="Enter product name"
          required
        />
        <button type="submit">Check Prices</button>
      </form>

      {loading && <p>Loading...</p>}

      {amazonPrice && <p>Amazon Price: {amazonPrice}</p>}
      {flipkartPrice && <p>Flipkart Price: {flipkartPrice}</p>}
    </div>
  );
}

export default App;

export function getProductFromItem(item) {
  return item?.product || item?.[item?.product_type] || item?.book || item?.cloth || null;
}

export function getProductName(product, type = "book") {
  if (!product) return type === "cloth" ? "Sản phẩm thời trang" : "Sách";
  return type === "cloth" ? product.name : product.title;
}

export function getProductSubtitle(product, type = "book") {
  if (!product) return "";
  if (type === "cloth") {
    return [product.brand, product.size_label, product.color].filter(Boolean).join(" • ");
  }
  return product.author || "";
}

export function getProductLink(type = "book", id) {
  return type === "cloth" ? `/clothes/${id}` : `/books/${id}`;
}

export function getProductEmoji(type = "book") {
  return type === "cloth" ? "👕" : "📚";
}

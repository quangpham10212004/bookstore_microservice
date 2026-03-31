import { Link } from "react-router-dom";
import { FiMinus, FiPlus, FiTrash2, FiShoppingBag } from "react-icons/fi";

import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import Loading from "../components/Loading";
import EmptyState from "../components/EmptyState";
import {
  getProductEmoji,
  getProductFromItem,
  getProductLink,
  getProductName,
  getProductSubtitle,
} from "../utils/product";

export default function CartPage() {
  const { cart, loading, updateItem, removeItem } = useCart();
  const { isAuthenticated } = useAuth();

  const formatPrice = (price) => {
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
    }).format(price);
  };

  if (!isAuthenticated) {
    return (
      <div className="container mx-auto px-4 py-16">
        <EmptyState
          icon={FiShoppingBag}
          title="Vui lòng đăng nhập"
          description="Đăng nhập để xem giỏ hàng của bạn"
          action={
            <Link to="/login" className="btn-primary">
              Đăng nhập
            </Link>
          }
        />
      </div>
    );
  }

  if (loading) return <Loading />;

  if (cart.items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-16">
        <EmptyState
          icon={FiShoppingBag}
          title="Giỏ hàng trống"
          description="Bạn chưa có sản phẩm nào trong giỏ hàng"
          action={
            <Link to="/" className="btn-primary">
              Mua sắm ngay
            </Link>
          }
        />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Giỏ hàng</h1>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-4">
          {cart.items.map((item) => (
            (() => {
              const product = getProductFromItem(item);
              const productName = getProductName(product, item.product_type);
              const productSubtitle = getProductSubtitle(product, item.product_type);
              const productLink = getProductLink(item.product_type, item.product_id);

              return (
                <div
                  key={`${item.product_type}-${item.product_id}`}
                  className="bg-white rounded-xl p-4 shadow-sm ring-1 ring-slate-100 flex gap-4"
                >
                  <Link
                    to={productLink}
                    className="w-24 h-32 bg-gray-100 rounded-lg flex-shrink-0 overflow-hidden"
                  >
                    {product?.image_url ? (
                      <img
                        src={product.image_url}
                        alt={productName}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary-100 to-accent-100">
                        <span className="text-3xl">{getProductEmoji(item.product_type)}</span>
                      </div>
                    )}
                  </Link>

                  <div className="flex-grow">
                    <Link
                      to={productLink}
                      className="font-semibold text-gray-800 hover:text-accent-700 line-clamp-2"
                    >
                      {productName}
                    </Link>
                    <p className="text-gray-500 text-sm mt-1">{productSubtitle}</p>

                    <div className="mt-4 flex items-center justify-between">
                      <div className="flex items-center border rounded-lg">
                        <button
                          onClick={() =>
                            updateItem(
                              item.product_id,
                              Math.max(1, item.quantity - 1),
                              item.product_type,
                            )
                          }
                          className="p-2 hover:bg-gray-100 transition-colors"
                        >
                          <FiMinus className="w-4 h-4" />
                        </button>
                        <span className="px-3 font-medium">{item.quantity}</span>
                        <button
                          onClick={() =>
                            updateItem(item.product_id, item.quantity + 1, item.product_type)
                          }
                          className="p-2 hover:bg-gray-100 transition-colors"
                        >
                          <FiPlus className="w-4 h-4" />
                        </button>
                      </div>

                      <span className="font-bold text-primary-700">
                        {product && formatPrice(product.price * item.quantity)}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={() => removeItem(item.product_id, item.product_type)}
                    className="p-2 text-gray-400 hover:text-red-500 transition-colors self-start"
                  >
                    <FiTrash2 className="w-5 h-5" />
                  </button>
                </div>
              );
            })()
          ))}
        </div>

        {/* Summary */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl p-6 shadow-sm ring-1 ring-slate-100 sticky top-24">
            <h2 className="font-semibold text-gray-800 text-lg mb-4">
              Tóm tắt đơn hàng
            </h2>

            <div className="space-y-3 border-b pb-4 mb-4">
              <div className="flex justify-between text-gray-600">
                <span>Tạm tính ({cart.items.length} sản phẩm)</span>
                <span>{formatPrice(cart.total)}</span>
              </div>
              <div className="flex justify-between text-gray-600">
                <span>Phí vận chuyển</span>
                <span className="text-green-600">Miễn phí</span>
              </div>
            </div>

            <div className="flex justify-between text-lg font-bold text-gray-800 mb-6">
              <span>Tổng cộng</span>
              <span className="text-primary-700">
                {formatPrice(cart.total)}
              </span>
            </div>

            <Link
              to="/checkout"
              className="btn-primary w-full text-center block"
            >
              Tiến hành thanh toán
            </Link>

            <Link
              to="/"
              className="block text-center text-accent-700 hover:text-accent-800 mt-4"
            >
              Tiếp tục mua sắm
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import { cartService } from "../services";
import { useAuth } from "./AuthContext";
import { toast } from "react-toastify";

const CartContext = createContext(null);

export function CartProvider({ children }) {
  const { customer, isAuthenticated } = useAuth();
  const [cart, setCart] = useState({ items: [], total: 0 });
  const [loading, setLoading] = useState(false);

  const fetchCart = useCallback(async () => {
    if (!isAuthenticated || !customer?.id) return;

    setLoading(true);
    try {
      const response = await cartService.getCart(customer.id);
      const cartData = response.data;

      const itemsWithProducts = (cartData.items || []).map((item) => ({
        ...item,
        product: item.product || item[item.product_type] || item.book || item.cloth || null,
      }));

      const total = itemsWithProducts.reduce((sum, item) => {
        if (item.product) {
          return sum + parseFloat(item.product.price) * item.quantity;
        }
        return sum;
      }, 0);

      setCart({ items: itemsWithProducts, total });
    } catch (error) {
      // Cart không tồn tại - sẽ tự tạo khi thêm item
      setCart({ items: [], total: 0 });
    } finally {
      setLoading(false);
    }
  }, [customer?.id, isAuthenticated]);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const addItem = async (productId, quantity = 1, productType = "book") => {
    if (!isAuthenticated) {
      toast.warning("Vui lòng đăng nhập để thêm vào giỏ hàng");
      return false;
    }

    try {
      await cartService.addItem(customer.id, productId, quantity, productType);
      await fetchCart();
      toast.success("Đã thêm vào giỏ hàng");
      return true;
    } catch (error) {
      toast.error(error.response?.data?.error || "Không thể thêm vào giỏ hàng");
      return false;
    }
  };

  const updateItem = async (productId, quantity, productType = "book") => {
    try {
      await cartService.updateItem(customer.id, productId, quantity, productType);
      await fetchCart();
      return true;
    } catch (error) {
      toast.error("Không thể cập nhật số lượng");
      return false;
    }
  };

  const removeItem = async (productId, productType = "book") => {
    try {
      await cartService.removeItem(customer.id, productId, productType);
      await fetchCart();
      toast.success("Đã xóa khỏi giỏ hàng");
      return true;
    } catch (error) {
      toast.error("Không thể xóa sản phẩm");
      return false;
    }
  };

  const clearCart = async () => {
    try {
      await cartService.clearCart(customer.id);
      setCart({ items: [], total: 0 });
      return true;
    } catch (error) {
      toast.error("Không thể xóa giỏ hàng");
      return false;
    }
  };

  const itemCount = cart.items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        cart,
        loading,
        itemCount,
        addItem,
        updateItem,
        removeItem,
        clearCart,
        fetchCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
};

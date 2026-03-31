import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  FiHeart,
  FiMinus,
  FiPlus,
  FiShare2,
  FiShoppingCart,
  FiStar,
} from "react-icons/fi";
import { toast } from "react-toastify";

import { catalogService, clothService, commentService } from "../services";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";
import Loading from "../components/Loading";

export default function ClothDetailPage() {
  const { id } = useParams();
  const { addItem } = useCart();
  const { isAuthenticated, customer } = useAuth();

  const [cloth, setCloth] = useState(null);
  const [catalog, setCatalog] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [activeTab, setActiveTab] = useState("description");
  const [newComment, setNewComment] = useState({ rating: 5, content: "" });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const clothRes = await clothService.getById(id);
        setCloth(clothRes.data);

        if (clothRes.data.catalog_id) {
          try {
            const catalogRes = await catalogService.getById(clothRes.data.catalog_id);
            setCatalog(catalogRes.data);
          } catch {}
        }

        try {
          const commentsRes = await commentService.getByCloth(id);
          setComments(
            commentsRes.data.reviews || commentsRes.data.results || commentsRes.data || [],
          );
        } catch {}
      } catch (error) {
        console.error("Error fetching cloth:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const formatPrice = (price) =>
    new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
    }).format(price);

  const handleAddToCart = async () => {
    const success = await addItem(cloth.id, quantity, "cloth");
    if (success) setQuantity(1);
  };

  const handleSubmitComment = async (e) => {
    e.preventDefault();
    if (!isAuthenticated) {
      toast.warning("Vui lòng đăng nhập để bình luận");
      return;
    }

    try {
      await commentService.create({
        cloth_id: parseInt(id, 10),
        customer_id: customer.id,
        rating: newComment.rating,
        content: newComment.content,
      });

      const commentsRes = await commentService.getByCloth(id);
      setComments(
        commentsRes.data.reviews || commentsRes.data.results || commentsRes.data || [],
      );
      setNewComment({ rating: 5, content: "" });
      toast.success("Đã thêm bình luận");
    } catch {
      toast.error("Không thể thêm bình luận");
    }
  };

  if (loading) return <Loading />;
  if (!cloth) {
    return <div className="container mx-auto px-4 py-8">Không tìm thấy sản phẩm</div>;
  }

  const avgRating =
    comments.length > 0
      ? (comments.reduce((sum, comment) => sum + comment.rating, 0) / comments.length).toFixed(1)
      : 0;

  return (
    <div className="container mx-auto px-4 py-8">
      <nav className="text-sm text-gray-500 mb-6">
        <Link to="/" className="hover:text-accent-700">
          Trang chủ
        </Link>
        <span className="mx-2">/</span>
        <Link to="/clothes" className="hover:text-accent-700">
          Quần áo
        </Link>
        {catalog && (
          <>
            <span className="mx-2">/</span>
            <Link to={`/clothes?catalog=${catalog.id}`} className="hover:text-accent-700">
              {catalog.name}
            </Link>
          </>
        )}
        <span className="mx-2">/</span>
        <span className="text-gray-800">{cloth.name}</span>
      </nav>

      <div className="bg-white rounded-xl shadow-sm ring-1 ring-slate-100 p-6 md:p-8">
        <div className="grid md:grid-cols-2 gap-8">
          <div className="aspect-[3/4] bg-gray-100 rounded-xl overflow-hidden">
            {cloth.image_url ? (
              <img src={cloth.image_url} alt={cloth.name} className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-100 to-orange-100">
                <span className="text-9xl">👕</span>
              </div>
            )}
          </div>

          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">{cloth.name}</h1>
            <p className="text-gray-500 text-lg mb-4">
              {[
                cloth.brand,
                cloth.gender,
                cloth.size_label && `Size ${cloth.size_label}`,
                cloth.color,
              ]
                .filter(Boolean)
                .join(" • ")}
            </p>

            <div className="flex items-center gap-2 mb-4">
              <div className="flex text-yellow-400">
                {[1, 2, 3, 4, 5].map((star) => (
                  <FiStar
                    key={star}
                    className={`w-5 h-5 ${star <= avgRating ? "fill-current" : ""}`}
                  />
                ))}
              </div>
              <span className="text-gray-500">({comments.length} đánh giá)</span>
            </div>

            <div className="mb-6">
              <span className="text-4xl font-bold text-primary-700">
                {formatPrice(cloth.price)}
              </span>
            </div>

            <div className="mb-6">
              {cloth.stock > 0 ? (
                <span className="inline-flex items-center px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                  Còn {cloth.stock} sản phẩm
                </span>
              ) : (
                <span className="inline-flex items-center px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm">
                  Hết hàng
                </span>
              )}
            </div>

            <div className="flex items-center gap-4 mb-6">
              <span className="text-gray-600">Số lượng:</span>
              <div className="flex items-center border rounded-lg">
                <button
                  onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                  className="p-3 hover:bg-gray-100 transition-colors"
                >
                  <FiMinus />
                </button>
                <span className="px-4 font-medium">{quantity}</span>
                <button
                  onClick={() => setQuantity((q) => Math.min(cloth.stock, q + 1))}
                  className="p-3 hover:bg-gray-100 transition-colors"
                >
                  <FiPlus />
                </button>
              </div>
            </div>

            <div className="flex flex-wrap gap-4 mb-6">
              <button
                onClick={handleAddToCart}
                disabled={cloth.stock === 0}
                className="btn-primary flex items-center gap-2 flex-grow md:flex-grow-0"
              >
                <FiShoppingCart className="w-5 h-5" />
                {cloth.stock === 0 ? "Hết hàng" : "Thêm vào giỏ"}
              </button>
              <button className="btn-secondary p-3">
                <FiHeart className="w-5 h-5" />
              </button>
              <button className="btn-secondary p-3">
                <FiShare2 className="w-5 h-5" />
              </button>
            </div>

            <div className="border-t pt-6 space-y-2 text-sm text-gray-500">
              <p>
                <span className="font-medium text-gray-700">SKU:</span> {cloth.sku}
              </p>
              <p>
                <span className="font-medium text-gray-700">Chất liệu:</span>{" "}
                {cloth.material || "Đang cập nhật"}
              </p>
              {catalog && (
                <p>
                  <span className="font-medium text-gray-700">Danh mục:</span> {catalog.name}
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="mt-10 border-t pt-8">
          <div className="flex gap-4 mb-6">
            <button
              onClick={() => setActiveTab("description")}
              className={`px-4 py-2 rounded-lg ${activeTab === "description" ? "bg-primary-100 text-primary-700" : "text-gray-500"}`}
            >
              Mô tả
            </button>
            <button
              onClick={() => setActiveTab("reviews")}
              className={`px-4 py-2 rounded-lg ${activeTab === "reviews" ? "bg-primary-100 text-primary-700" : "text-gray-500"}`}
            >
              Đánh giá ({comments.length})
            </button>
          </div>

          {activeTab === "description" ? (
            <div className="prose max-w-none text-gray-600">
              <p>{cloth.description || "Chưa có mô tả cho sản phẩm này."}</p>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="space-y-4">
                {comments.map((comment) => (
                  <div key={comment.id} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">Khách hàng #{comment.customer_id}</span>
                      <span className="text-sm text-gray-500">{comment.rating}/5</span>
                    </div>
                    <p className="text-gray-600">{comment.content || comment.comment}</p>
                  </div>
                ))}
              </div>

              <form onSubmit={handleSubmitComment} className="border rounded-xl p-4 space-y-4">
                <h3 className="font-semibold text-gray-800">Viết đánh giá</h3>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Số sao</label>
                  <select
                    value={newComment.rating}
                    onChange={(e) =>
                      setNewComment((prev) => ({ ...prev, rating: parseInt(e.target.value, 10) }))
                    }
                    className="input-field"
                  >
                    {[5, 4, 3, 2, 1].map((rating) => (
                      <option key={rating} value={rating}>
                        {rating} sao
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Nội dung</label>
                  <textarea
                    value={newComment.content}
                    onChange={(e) =>
                      setNewComment((prev) => ({ ...prev, content: e.target.value }))
                    }
                    rows={4}
                    className="input-field"
                    placeholder="Chia sẻ cảm nhận của bạn về sản phẩm..."
                  />
                </div>
                <button type="submit" className="btn-primary">
                  Gửi đánh giá
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

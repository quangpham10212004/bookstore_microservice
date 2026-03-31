import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { FiFilter, FiGrid, FiList } from "react-icons/fi";

import { catalogService, clothService } from "../services";
import { useCart } from "../context/CartContext";
import ClothCard from "../components/ClothCard";
import EmptyState from "../components/EmptyState";
import Loading from "../components/Loading";

export default function ClothesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [clothes, setClothes] = useState([]);
  const [catalogs, setCatalogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState("grid");
  const [showFilters, setShowFilters] = useState(false);

  const catalogId = searchParams.get("catalog");
  const searchQuery = searchParams.get("search");
  const sortBy = searchParams.get("sort") || "newest";

  useEffect(() => {
    const fetchCatalogs = async () => {
      try {
        const response = await catalogService.getAll();
        setCatalogs(response.data.results || response.data || []);
      } catch (error) {
        console.error("Error fetching catalogs:", error);
      }
    };
    fetchCatalogs();
  }, []);

  useEffect(() => {
    const fetchClothes = async () => {
      setLoading(true);
      try {
        const params = {};
        if (catalogId) params.catalog_id = catalogId;
        if (searchQuery) params.search = searchQuery;
        if (sortBy === "newest") params.ordering = "-created_at";
        if (sortBy === "price_low") params.ordering = "price";
        if (sortBy === "price_high") params.ordering = "-price";

        const response = await clothService.getAll(params);
        setClothes(response.data.results || response.data || []);
      } catch (error) {
        console.error("Error fetching clothes:", error);
        setClothes([]);
      } finally {
        setLoading(false);
      }
    };
    fetchClothes();
  }, [catalogId, searchQuery, sortBy]);

  const handleCatalogChange = (id) => {
    if (id) {
      searchParams.set("catalog", id);
    } else {
      searchParams.delete("catalog");
    }
    setSearchParams(searchParams);
  };

  const handleSortChange = (sort) => {
    searchParams.set("sort", sort);
    setSearchParams(searchParams);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">
            {searchQuery ? `Kết quả thời trang: "${searchQuery}"` : "Tất cả quần áo"}
          </h1>
          <p className="text-gray-500 mt-1">{clothes.length} sản phẩm</p>
        </div>

        <div className="flex items-center gap-4">
          <select
            value={sortBy}
            onChange={(e) => handleSortChange(e.target.value)}
            className="input-field w-auto"
          >
            <option value="newest">Mới nhất</option>
            <option value="price_low">Giá thấp - cao</option>
            <option value="price_high">Giá cao - thấp</option>
          </select>

          <div className="flex border border-slate-200 rounded-lg overflow-hidden shadow-sm">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-2 ${viewMode === "grid" ? "bg-primary-600 text-white" : "bg-white text-gray-600 hover:text-accent-700"}`}
            >
              <FiGrid className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`p-2 ${viewMode === "list" ? "bg-primary-600 text-white" : "bg-white text-gray-600 hover:text-accent-700"}`}
            >
              <FiList className="w-5 h-5" />
            </button>
          </div>

          <button
            onClick={() => setShowFilters(!showFilters)}
            className="md:hidden p-2 border border-slate-200 rounded-lg text-accent-700"
          >
            <FiFilter className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="flex gap-8">
        <aside className={`w-64 flex-shrink-0 ${showFilters ? "block" : "hidden"} md:block`}>
          <div className="bg-white rounded-xl p-6 shadow-sm ring-1 ring-slate-100">
            <h3 className="font-semibold text-gray-800 mb-4">Danh mục</h3>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => handleCatalogChange(null)}
                  className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                    !catalogId
                      ? "bg-primary-100 text-primary-700 font-medium"
                      : "hover:bg-accent-50 hover:text-accent-700"
                  }`}
                >
                  Tất cả
                </button>
              </li>
              {catalogs.map((catalog) => (
                <li key={catalog.id}>
                  <button
                    onClick={() => handleCatalogChange(catalog.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                      catalogId == catalog.id
                        ? "bg-primary-100 text-primary-700 font-medium"
                        : "hover:bg-accent-50 hover:text-accent-700"
                    }`}
                  >
                    {catalog.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </aside>

        <div className="flex-grow">
          {loading ? (
            <Loading />
          ) : clothes.length === 0 ? (
            <EmptyState
              title="Không tìm thấy quần áo"
              description="Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm"
            />
          ) : viewMode === "grid" ? (
            <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {clothes.map((cloth) => (
                <ClothCard key={cloth.id} cloth={cloth} />
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {clothes.map((cloth) => (
                <ClothListItem key={cloth.id} cloth={cloth} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function ClothListItem({ cloth }) {
  const { addItem } = useCart();

  const formatPrice = (price) =>
    new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
    }).format(price);

  return (
    <div className="bg-white rounded-xl p-4 shadow-sm ring-1 ring-slate-100 flex gap-4">
      <div className="w-32 h-40 bg-gray-100 rounded-lg flex-shrink-0 overflow-hidden">
        {cloth.image_url ? (
          <img src={cloth.image_url} alt={cloth.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-100 to-orange-100">
            <span className="text-4xl">👕</span>
          </div>
        )}
      </div>
      <div className="flex-grow">
        <h3 className="font-semibold text-gray-800 text-lg">{cloth.name}</h3>
        <p className="text-gray-500">
          {[cloth.brand, cloth.size_label, cloth.color].filter(Boolean).join(" • ")}
        </p>
        <p className="text-gray-600 text-sm mt-2 line-clamp-2">{cloth.description}</p>
        <div className="mt-4 flex items-center justify-between">
          <span className="text-xl font-bold text-primary-700">{formatPrice(cloth.price)}</span>
          <button
            onClick={() => addItem(cloth.id, 1, "cloth")}
            disabled={cloth.stock === 0}
            className="btn-primary"
          >
            {cloth.stock === 0 ? "Hết hàng" : "Thêm vào giỏ"}
          </button>
        </div>
      </div>
    </div>
  );
}

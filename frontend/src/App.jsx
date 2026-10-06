import React, { useState, useEffect } from 'react';
import {
  Sparkles, Camera, Mic, ShoppingBag, Layers, Package, Users, Sliders,
  TrendingUp, Send, CheckCircle, FileText, ArrowRight, ShieldCheck, RefreshCw,
  Globe, CreditCard, Check, X, Star, MapPin, Search, Filter, Heart,
  ShoppingCart, ChevronRight, MessageSquare, Award, ArrowUpRight, HelpCircle,
  Truck, ShieldAlert, Zap, Compass, Store, Settings, PieChart, Tag, RefreshCcw, Home
} from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

export default function App() {
  // Tab Persistence: Customer vs Artisan views
  const getInitialMode = () => {
    return localStorage.getItem('kaarvo_app_mode') || 'customer';
  };

  const getInitialCustomerTab = () => {
    const hash = window.location.hash.replace('#', '');
    const valid = ['home', 'shop', 'ai_ask', 'stories'];
    if (valid.includes(hash)) return hash;
    return localStorage.getItem('kaarvo_customer_tab') || 'home';
  };

  const getInitialArtisanTab = () => {
    const hash = window.location.hash.replace('#', '');
    const valid = ['dashboard', 'copilot', 'studio', 'orders', 'customers', 'insights', 'marketing', 'settings'];
    if (valid.includes(hash)) return hash;
    return localStorage.getItem('kaarvo_artisan_tab') || 'dashboard';
  };

  const [mode, setMode] = useState(getInitialMode);
  const [customerTab, setCustomerTab] = useState(getInitialCustomerTab);
  const [artisanTab, setArtisanTab] = useState(getInitialArtisanTab);

  // DB State
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  // Cart & Wishlist State
  const [cartItems, setCartItems] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('kaarvo_cart')) || [];
    } catch (e) {
      return [];
    }
  });
  const [wishlist, setWishlist] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);

  // Customer AI Search & Shopping State
  const [customerSearchQuery, setCustomerSearchQuery] = useState('');
  const [activeCategoryFilter, setActiveCategoryFilter] = useState('All');
  const [aiShoppingInput, setAiShoppingInput] = useState('');
  const [aiShoppingHistory, setAiShoppingHistory] = useState([
    {
      sender: 'ai',
      text: 'Namaste! I am your Kaarvo AI Craft Assistant. Ask me to find authentic Indian handicrafts, unique gifts, or products within your budget!',
      recommendedIds: [1, 2]
    }
  ]);
  const [aiShoppingLoading, setAiShoppingLoading] = useState(false);

  // Checkout State
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [checkoutStep, setCheckoutStep] = useState(1);
  const [checkoutData, setCheckoutData] = useState({
    name: 'Rohan Sharma',
    phone: '+91 98765 43210',
    address: 'Flat 402, Royal Residency, Malviya Nagar',
    city: 'Jaipur',
    pincode: '302017',
    paymentMethod: 'UPI'
  });
  const [isPlacingOrder, setIsPlacingOrder] = useState(false);

  // --- PILLAR 1: AI STUDIO IMAGE ENHANCER STATES ---
  const [rawImageFile, setRawImageFile] = useState(null);
  const [enhancedImage, setEnhancedImage] = useState(null);
  const [imageEnhancing, setImageEnhancing] = useState(false);

  // --- PILLAR 2: MULTILINGUAL VOICE AUTO-CATALOGER STATES ---
  const [voiceText, setVoiceText] = useState('Yeh Jaipur ki pure terracotta clay water pot hai, hand-carved floral design ke sath, 1.5 liter capacity.');
  const [selectedLanguage, setSelectedLanguage] = useState('hi-IN');
  const [isRecording, setIsRecording] = useState(false);
  const [extractedEntities, setExtractedEntities] = useState(null);
  const [generatedCatalog, setGeneratedCatalog] = useState(null);
  const [cataloging, setCataloging] = useState(false);

  // --- PILLAR 3: DYNAMIC COST-PLUS PRICING ASSISTANT STATES ---
  const [materialCost, setMaterialCost] = useState(180);
  const [laborCost, setLaborCost] = useState(150);
  const [craftCategory, setCraftCategory] = useState('Pottery / Terracotta');
  const [pricingResult, setPricingResult] = useState(null);

  // Copilot State
  const [copilotInput, setCopilotInput] = useState('');
  const [copilotLoading, setCopilotLoading] = useState(false);
  const [copilotHistory, setCopilotHistory] = useState([
    { sender: 'ai', content: 'Namaste! I am your Kaarvo Artisan Copilot. How can I help grow your craft business today?' }
  ]);

  // Toast Notification
  const [toastMessage, setToastMessage] = useState(null);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  // Category Markups
  const categoryMarkups = {
    'Textiles / Handloom': { min: 0.30, max: 0.45, label: '30% – 45%' },
    'Pottery / Terracotta': { min: 0.40, max: 0.60, label: '40% – 60%' },
    'Metal craft': { min: 0.35, max: 0.55, label: '35% – 55%' },
    'Woodwork': { min: 0.35, max: 0.50, label: '35% – 50%' },
    'Jewelry (traditional)': { min: 0.45, max: 0.70, label: '45% – 70%' }
  };

  // Default Sample Products for Rich Desktop Grid Rendering
  const defaultProducts = [
    {
      id: 1,
      title: 'Handcrafted Terracotta Cooling Water Pitcher',
      category: 'Pottery / Terracotta',
      price: 480,
      originalPrice: 650,
      rating: 4.9,
      reviewsCount: 38,
      artisan: 'Ramswaroop Prajapat',
      location: 'Jaipur, Rajasthan',
      description: '1.5L natural eco-friendly cooling clay water jug handcrafted using traditional wheel pottery and relief carving techniques.',
      materials: 'Natural Clay, Organic Herbal Polish',
      craftStory: 'Passed down through 4 generations of Prajapat potters in Rajasthan, this pitcher naturally keeps water cool through porous clay evaporation.',
      image: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80',
      badge: 'Bestseller'
    },
    {
      id: 2,
      title: 'Handwoven Pure Chanderi Silk Saree with Zari Motifs',
      category: 'Textiles / Handloom',
      price: 2450,
      originalPrice: 3200,
      rating: 4.8,
      reviewsCount: 52,
      artisan: 'Sunita Devi Weaver Guild',
      location: 'Chanderi, Madhya Pradesh',
      description: 'Authentic lightweight handloom Chanderi silk saree featuring delicate gold zari peacocks woven over 14 days.',
      materials: 'Mulberry Silk, Gold Zari Thread',
      craftStory: 'Woven on traditional pit looms in Chanderi, celebrated for its translucent texture and Royal Maratha heritage patronage.',
      image: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80',
      badge: 'Heritage Craft'
    },
    {
      id: 3,
      title: 'Solid Brass Dhokra Lost-Wax Tribal Sculpture',
      category: 'Metal craft',
      price: 980,
      originalPrice: 1250,
      rating: 5.0,
      reviewsCount: 19,
      artisan: 'Bishnu Jhara',
      location: 'Bastar, Chhattisgarh',
      description: 'Ancient 4,000-year-old lost-wax casting technique non-ferrous metal statue of traditional tribal musicians.',
      materials: 'Recycled Brass, Beeswax, Clay Mold',
      craftStory: 'Every Dhokra piece is entirely unique since the clay and wax mold is broken open to release the cooled metal figurine.',
      image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80',
      badge: '4,000 Yr Heritage'
    },
    {
      id: 4,
      title: 'Carved Sheesham Wood Floral Jewelry Trunk',
      category: 'Woodwork',
      price: 1350,
      originalPrice: 1800,
      rating: 4.7,
      reviewsCount: 24,
      artisan: 'Mohammad Rashid Woodcarvers',
      location: 'Saharanpur, Uttar Pradesh',
      description: 'Hand-carved Indian Rosewood box with velvet lining and brass latch for heirloom jewelry storage.',
      materials: 'Sheesham Wood, Brass Hardware, Velvet',
      craftStory: 'Saharanpur is famous worldwide for intricate lattice jaali woodwork carved with hand chisels.',
      image: 'https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=800&q=80',
      badge: 'Fair Trade'
    },
    {
      id: 5,
      title: 'Traditional Kundan Meenakari Peacock Earrings',
      category: 'Jewelry (traditional)',
      price: 1120,
      originalPrice: 1500,
      rating: 4.9,
      reviewsCount: 31,
      artisan: 'Meenakari Guild Jaipur',
      location: 'Jaipur, Rajasthan',
      description: 'Hand-enameled Royal Rajasthani peacock earrings studded with semi-precious stone embellishments.',
      materials: 'Brass Alloy, Enamel Color, Pearls',
      craftStory: 'Brought to Jaipur by Raja Man Singh I, Meenakari is the art of fusing vibrant colors onto intricate metal grooves.',
      image: 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=800&q=80',
      badge: 'Royal Heritage'
    },
    {
      id: 6,
      title: 'Blue Pottery Handpainted Decorative Wall Plate',
      category: 'Pottery / Terracotta',
      price: 850,
      originalPrice: 1100,
      rating: 4.8,
      reviewsCount: 29,
      artisan: 'Kripal Blue Pottery Studio',
      location: 'Jaipur, Rajasthan',
      description: 'Turquoise quartz clay decorative plate handpainted with Persian floral arabesque motifs.',
      materials: 'Quartz Powder, Multani Mitti, Oxide Colors',
      craftStory: 'Unlike clay pottery, Jaipur Blue Pottery uses quartz stone powder which gives it its distinct glassy glaze.',
      image: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80',
      badge: 'GI Tagged'
    },
    {
      id: 7,
      title: 'Bagh Block Print Organic Cotton Dupatta',
      category: 'Textiles / Handloom',
      price: 950,
      originalPrice: 1300,
      rating: 4.9,
      reviewsCount: 41,
      artisan: 'Khatri Artisan Guild',
      location: 'Dhar, Madhya Pradesh',
      description: 'Natural vegetable dyed hand block printed cotton stole made with teak wood blocks.',
      materials: '100% Organic Cotton, Natural Madder Root Dye',
      craftStory: 'Bagh prints use 100% natural vegetable dyes processed in Bagh river water rich in copper content.',
      image: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80',
      badge: 'Eco Friendly'
    },
    {
      id: 8,
      title: 'Bidriware Silver Inlay Brass Incense Burner',
      category: 'Metal craft',
      price: 1650,
      originalPrice: 2200,
      rating: 5.0,
      reviewsCount: 16,
      artisan: 'Bidar Craft Collective',
      location: 'Bidar, Karnataka',
      description: 'Zinc-copper black metal vessel inlaid with pure 99.9% silver wire detailing.',
      materials: 'Zinc Alloy, Pure Silver Wire, Bidar Soil',
      craftStory: 'Bidriware gets its jet black oxidized color from unique historical soil found inside Bidar Fort.',
      image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80',
      badge: 'Royal Craft'
    }
  ];

  // Fetch DB data
  const fetchData = async () => {
    setLoading(true);
    try {
      const pRes = await fetch(`${API_BASE}/products`);
      if (pRes.ok) {
        const data = await pRes.json();
        if (Array.isArray(data) && data.length > 0) {
          setProducts(data);
        } else {
          setProducts(defaultProducts);
        }
      } else {
        setProducts(defaultProducts);
      }

      const oRes = await fetch(`${API_BASE}/orders`);
      if (oRes.ok) setOrders(await oRes.json());
    } catch (err) {
      console.error(err);
      setProducts(defaultProducts);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    calculatePricing(180, 150, 'Pottery / Terracotta');
  }, []);

  useEffect(() => {
    localStorage.setItem('kaarvo_cart', JSON.stringify(cartItems));
  }, [cartItems]);

  const switchMode = (newMode) => {
    setMode(newMode);
    localStorage.setItem('kaarvo_app_mode', newMode);
  };

  const switchCustomerTab = (tab) => {
    setCustomerTab(tab);
    localStorage.setItem('kaarvo_customer_tab', tab);
    window.location.hash = tab;
  };

  const switchArtisanTab = (tab) => {
    setArtisanTab(tab);
    localStorage.setItem('kaarvo_artisan_tab', tab);
    window.location.hash = tab;
  };

  // Cart operations
  const addToCart = (product, e) => {
    if (e) e.stopPropagation();
    setCartItems(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item);
      }
      return [...prev, { ...product, quantity: 1 }];
    });
    showToast(`Added "${product.title.slice(0, 25)}..." to Cart!`);
  };

  const updateCartQty = (id, delta) => {
    setCartItems(prev => prev.map(item => {
      if (item.id === id) {
        const newQty = item.quantity + delta;
        return newQty > 0 ? { ...item, quantity: newQty } : null;
      }
      return item;
    }).filter(Boolean));
  };

  const removeFromCart = (id) => {
    setCartItems(prev => prev.filter(item => item.id !== id));
  };

  const toggleWishlist = (id, e) => {
    if (e) e.stopPropagation();
    setWishlist(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);
  };

  // Calculations
  const cartSubtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const shippingFee = cartSubtotal > 999 || cartSubtotal === 0 ? 0 : 99;
  const cartTotal = cartSubtotal + shippingFee;

  // Pricing formula
  const calculatePricing = (mat, lab, cat) => {
    const markup = categoryMarkups[cat] || categoryMarkups['Pottery / Terracotta'];
    const baseCost = (parseFloat(mat) || 0) + (parseFloat(lab) || 0);
    const minP = Math.round((baseCost * (1 + markup.min)) / 10) * 10;
    const maxP = Math.round((baseCost * (1 + markup.max)) / 10) * 10;

    setPricingResult({
      baseCost,
      min: minP,
      max: maxP,
      markupRange: markup.label
    });
  };

  // PILLAR 1: Image Enhancer Simulation
  const handleEnhanceImage = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setRawImageFile(URL.createObjectURL(file));
    setImageEnhancing(true);

    setTimeout(() => {
      setEnhancedImage('https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80');
      setImageEnhancing(false);
      showToast('✨ OpenCV Background Removal & Lighting Balance Completed!');
    }, 1200);
  };

  // PILLAR 2: Multilingual Voice Auto-Cataloger
  const handleGenerateCatalogFromVoice = async () => {
    setCataloging(true);
    try {
      setTimeout(() => {
        const entities = {
          material: 'Pure Red Clay / Terracotta',
          technique: 'Hand-Carved Relief Motifs',
          region: 'Jaipur, Rajasthan',
          use_case: 'Eco-friendly Natural Water Storage'
        };

        const catalog = {
          product_id: `KAARVO-${Math.floor(100000 + Math.random() * 900000)}`,
          artisan_id: 'ART-00456',
          category: 'Pottery / Terracotta',
          descriptor: {
            name: 'Handcrafted Terracotta Water Jug — Jaipur Craft',
            long_desc: 'Authentic 1.5L natural red clay jug handcrafted by master artisans in Jaipur. Eco-friendly, naturally cooling, featuring traditional hand-carved relief motifs.',
            images: [enhancedImage || 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80']
          },
          price: {
            currency: 'INR',
            suggested_range: { min: pricingResult?.min || 480, max: pricingResult?.max || 550 },
            breakdown: {
              material_cost: materialCost,
              labor_cost: laborCost,
              category_margin_pct: 40
            }
          },
          ondc_beckn_compliant: true
        };

        setExtractedEntities(entities);
        setGeneratedCatalog(catalog);
        setCataloging(false);
        showToast('✨ ONDC Beckn Catalog Schema Generated via Bhashini!');
      }, 1000);
    } catch (err) {
      console.error(err);
      setCataloging(false);
    }
  };

  // Save generated product to DB
  const handleSaveCatalogToDB = async () => {
    if (!generatedCatalog) return;
    try {
      const newP = {
        title: generatedCatalog.descriptor.name,
        description: generatedCatalog.descriptor.long_desc,
        price: generatedCatalog.price.suggested_range.min,
        category: generatedCatalog.category,
        status: 'published',
        material_cost: materialCost,
        labor_cost: laborCost,
        artisan: 'Ramswaroop Prajapat',
        location: 'Jaipur, Rajasthan',
        rating: 5.0,
        reviewsCount: 1,
        image: enhancedImage || 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80'
      };

      const res = await fetch(`${API_BASE}/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newP)
      });

      if (res.ok) {
        await fetchData();
      } else {
        setProducts(prev => [{ id: Date.now(), ...newP }, ...prev]);
      }
      showToast('🎉 Product Cataloged & Published Live to Kaarvo Store!');
      switchArtisanTab('dashboard');
    } catch (err) {
      console.error(err);
    }
  };

  // Customer AI Shopping query handler
  const handleAiShoppingQuery = (promptText) => {
    const q = promptText || aiShoppingInput;
    if (!q.trim()) return;

    setAiShoppingInput('');
    setAiShoppingLoading(true);

    setTimeout(() => {
      let recs = products.slice(0, 2);
      if (q.toLowerCase().includes('gift') || q.toLowerCase().includes('1500')) {
        recs = products.filter(p => p.price <= 1500);
      } else if (q.toLowerCase().includes('silk') || q.toLowerCase().includes('saree')) {
        recs = products.filter(p => p.category.includes('Textiles'));
      } else if (q.toLowerCase().includes('pottery') || q.toLowerCase().includes('terracotta')) {
        recs = products.filter(p => p.category.includes('Pottery'));
      }

      setAiShoppingHistory(prev => [
        ...prev,
        { sender: 'user', text: q },
        {
          sender: 'ai',
          text: `Based on your query "${q}", here are authentic handcrafted recommendations directly from verified Indian artisans:`,
          recommendedProducts: recs.length > 0 ? recs : products.slice(0, 2)
        }
      ]);
      setAiShoppingLoading(false);
    }, 800);
  };

  // Artisan Copilot Send
  const handleCopilotSend = (prompt) => {
    const q = prompt || copilotInput;
    if (!q.trim()) return;
    setCopilotHistory(prev => [...prev, { sender: 'artisan', content: q }]);
    setCopilotInput('');
    setCopilotLoading(true);

    setTimeout(() => {
      setCopilotHistory(prev => [
        ...prev,
        {
          sender: 'ai',
          content: `🤖 Kaarvo Copilot Recommendation: Analyzed your inventory and market trends for "${q}". Demand is up 24% for Rajasthan pottery. Recommended action: Increase pricing margin by 5% and publish a Diwali campaign.`
        }
      ]);
      setCopilotLoading(false);
    }, 700);
  };

  // Place Order
  const handlePlaceOrder = async () => {
    setIsPlacingOrder(true);
    try {
      const firstItem = cartItems[0] || products[0];
      const res = await fetch(`${API_BASE}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: firstItem.id,
          quantity: cartItems.length || 1,
          customer_name: checkoutData.name,
          shipping_address: `${checkoutData.address}, ${checkoutData.city} ${checkoutData.pincode}`
        })
      });

      let placedOrder;
      if (res.ok) {
        placedOrder = await res.json();
      } else {
        placedOrder = {
          id: `ORD-${Math.floor(1000 + Math.random() * 9000)}`,
          customer_name: checkoutData.name,
          total_price: cartTotal || 480,
          status: 'paid'
        };
      }

      setOrders(prev => [placedOrder, ...prev]);
      setCartItems([]);
      setIsPlacingOrder(false);
      setCheckoutStep(4);
      showToast('🎉 Order Placed Successfully!');
    } catch (err) {
      console.error(err);
      setIsPlacingOrder(false);
      setCheckoutStep(4);
      setCartItems([]);
    }
  };

  // Filtered products list for Customer Shop View
  const filteredProducts = products.filter(p => {
    const q = customerSearchQuery.toLowerCase();
    const matchesCategory = activeCategoryFilter === 'All' || p.category === activeCategoryFilter;
    const matchesSearch = !q || (
      p.title.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q) ||
      (p.artisan && p.artisan.toLowerCase().includes(q))
    );
    return matchesCategory && matchesSearch;
  });

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg-body)' }}>
      
      {/* GLOBAL TOP CONTROL BAR (MODE SWITCHER) */}
      <div style={{
        background: 'var(--bg-dark)',
        color: '#A8A29E',
        padding: '6px 28px',
        fontSize: '12px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '1px solid #292524'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ display: 'inline-block', width: '8px', height: '8px', borderRadius: '50%', background: '#10B981' }}></span>
          <span style={{ color: '#F5F5F4', fontWeight: '600' }}>Kaarvo AI Commerce OS</span>
          <span style={{ color: '#78716C' }}>• SIH26090 MoSJE Market Linkage</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', background: '#292524', padding: '3px', borderRadius: '20px' }}>
          <button
            onClick={() => switchMode('customer')}
            style={{
              background: mode === 'customer' ? 'var(--primary)' : 'transparent',
              color: mode === 'customer' ? '#FFFFFF' : '#A8A29E',
              border: 'none',
              padding: '4px 14px',
              borderRadius: '16px',
              fontSize: '11px',
              fontWeight: '700',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease'
            }}
          >
            <Store size={13} /> Customer Marketplace
          </button>
          <button
            onClick={() => switchMode('artisan')}
            style={{
              background: mode === 'artisan' ? 'var(--primary)' : 'transparent',
              color: mode === 'artisan' ? '#FFFFFF' : '#A8A29E',
              border: 'none',
              padding: '4px 14px',
              borderRadius: '16px',
              fontSize: '11px',
              fontWeight: '700',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease'
            }}
          >
            <Layers size={13} /> Artisan Business OS
          </button>
        </div>
      </div>

      {/* TOAST NOTIFICATION CONTAINER */}
      {toastMessage && (
        <div className="toast-container">
          <div className="toast-item">
            <CheckCircle size={16} color="#10B981" />
            <span>{toastMessage}</span>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODE 1: CUSTOMER MARKETPLACE & SHOPPING EXPERIENCE                        */}
      {/* ========================================================================= */}
      {mode === 'customer' && (
        <>
          {/* CUSTOMER STICKY NAVBAR */}
          <header style={{
            background: 'var(--bg-surface)',
            borderBottom: '1px solid var(--border-subtle)',
            padding: '16px 0',
            position: 'sticky',
            top: 0,
            zIndex: 100,
            boxShadow: 'var(--shadow-sm)'
          }}>
            <div className="container-wide" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              
              {/* BRAND LOGO */}
              <div
                onClick={() => switchCustomerTab('home')}
                style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '10px' }}
              >
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '12px',
                  background: 'var(--primary)',
                  color: '#FFF',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: '800',
                  fontSize: '22px'
                }}>
                  🪔
                </div>
                <div>
                  <div style={{ fontSize: '22px', fontWeight: '800', letterSpacing: '-0.02em', color: 'var(--text-main)', lineHeight: '1' }}>
                    Kaarvo<span style={{ color: 'var(--primary)' }}>.</span>
                  </div>
                  <div style={{ fontSize: '10px', fontWeight: '700', color: 'var(--text-muted)', letterSpacing: '0.05em', marginTop: '2px' }}>
                    CRAFTED BY HAND • AI POWERED
                  </div>
                </div>
              </div>

              {/* NAVIGATION LINKS */}
              <nav className="hide-mobile" style={{ display: 'flex', gap: '32px', alignItems: 'center' }}>
                {[
                  { id: 'home', label: 'Home' },
                  { id: 'shop', label: 'Explore Crafts' },
                  { id: 'ai_ask', label: '✨ Ask Kaarvo AI' },
                  { id: 'stories', label: 'Craft Stories' }
                ].map(item => (
                  <button
                    key={item.id}
                    onClick={() => switchCustomerTab(item.id)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      fontSize: '15px',
                      fontWeight: customerTab === item.id ? '700' : '500',
                      color: customerTab === item.id ? 'var(--primary)' : 'var(--text-secondary)',
                      cursor: 'pointer',
                      padding: '6px 0',
                      borderBottom: customerTab === item.id ? '2.5px solid var(--primary)' : '2.5px solid transparent',
                      transition: 'color 0.2s ease'
                    }}
                  >
                    {item.label}
                  </button>
                ))}
              </nav>

              {/* ACTIONS: WISHLIST & CART */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <button
                  onClick={() => switchCustomerTab('shop')}
                  style={{ background: 'var(--bg-subtle)', border: 'none', width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}
                >
                  <Search size={18} color="var(--text-secondary)" />
                </button>

                <button
                  onClick={() => setIsCartOpen(true)}
                  style={{
                    background: 'var(--primary-light)',
                    border: '1px solid var(--primary-border)',
                    color: 'var(--primary)',
                    padding: '9px 18px',
                    borderRadius: 'var(--radius-full)',
                    fontWeight: '700',
                    fontSize: '14px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                  }}
                >
                  <ShoppingCart size={17} />
                  <span>Cart</span>
                  {cartItems.length > 0 && (
                    <span style={{ background: 'var(--primary)', color: '#FFF', padding: '2px 8px', borderRadius: '10px', fontSize: '12px' }}>
                      {cartItems.reduce((a, b) => a + b.quantity, 0)}
                    </span>
                  )}
                </button>

                <button
                  className="btn-artisan-secondary hide-mobile"
                  onClick={() => switchMode('artisan')}
                  style={{ fontSize: '13px', padding: '9px 16px' }}
                >
                  Start Selling →
                </button>
              </div>
            </div>
          </header>

          {/* MAIN CUSTOMER BODY */}
          <main style={{ flex: 1 }}>

            {/* VIEW 1: CUSTOMER HOME PAGE */}
            {customerTab === 'home' && (
              <div>
                
                {/* 1. TWO-COLUMN HERO SECTION */}
                <section style={{
                  padding: '60px 0 80px',
                  background: 'linear-gradient(180deg, #FAF9F5 0%, #F3F1E9 100%)',
                  borderBottom: '1px solid var(--border-subtle)'
                }}>
                  <div className="container-wide">
                    <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: '48px', alignItems: 'center' }}>
                      
                      {/* LEFT HERO COLUMN */}
                      <div>
                        <span className="badge-tag badge-terracotta" style={{ marginBottom: '16px' }}>
                          🇮🇳 MoSJE & ONDC Verified Artisan Network
                        </span>
                        
                        <h1 className="font-serif" style={{ fontSize: '54px', fontWeight: '700', color: 'var(--text-main)', lineHeight: '1.12', marginBottom: '20px' }}>
                          Crafted by Hand. <br />
                          <span style={{ color: 'var(--primary)', fontStyle: 'italic' }}>Powered by AI.</span>
                        </h1>
                        
                        <p style={{ fontSize: '17px', color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '32px', maxWidth: '580px' }}>
                          Discover authentic handcrafted treasures directly from master Indian artisans. Powered by AI voice cataloging, fair trade pricing, and direct market linkage.
                        </p>

                        {/* HERO CTA BUTTONS */}
                        <div style={{ display: 'flex', gap: '14px', marginBottom: '40px', flexWrap: 'wrap' }}>
                          <button className="btn-artisan-primary" onClick={() => switchCustomerTab('shop')} style={{ padding: '14px 32px', fontSize: '16px' }}>
                            Explore Products <ArrowRight size={18} />
                          </button>
                          <button className="btn-artisan-secondary" onClick={() => switchMode('artisan')} style={{ padding: '14px 28px', fontSize: '15px' }}>
                            Start Selling
                          </button>
                        </div>

                        {/* VISUALLY IMPORTANT AI SEARCH BOX */}
                        <div className="card-artisan" style={{ padding: '14px 18px', background: '#FFFFFF', boxShadow: '0 12px 32px rgba(28, 25, 23, 0.08)' }}>
                          <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--primary)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <Sparkles size={16} /> ✨ Ask Kaarvo AI — What are you looking for?
                          </div>
                          
                          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <input
                              type="text"
                              value={customerSearchQuery}
                              onChange={(e) => setCustomerSearchQuery(e.target.value)}
                              onKeyDown={(e) => e.key === 'Enter' && switchCustomerTab('shop')}
                              placeholder="e.g. 'Find me a handmade gift under ₹1500'"
                              style={{ border: 'none', outline: 'none', flex: 1, fontSize: '14px', color: 'var(--text-main)', background: 'transparent' }}
                            />
                            <button
                              className="btn-artisan-primary"
                              onClick={() => switchCustomerTab('shop')}
                              style={{ padding: '10px 20px', fontSize: '13px' }}
                            >
                              Search
                            </button>
                          </div>

                          {/* SUGGESTION CHIPS */}
                          <div style={{ display: 'flex', gap: '8px', marginTop: '12px', flexWrap: 'wrap' }}>
                            {[
                              'Handmade gift under ₹1500',
                              'Traditional Indian crafts',
                              'Home decor',
                              'Wedding gifts'
                            ].map(chip => (
                              <button
                                key={chip}
                                onClick={() => {
                                  setCustomerSearchQuery(chip);
                                  switchCustomerTab('shop');
                                }}
                                style={{ background: 'var(--bg-subtle)', border: '1px solid var(--border-subtle)', borderRadius: '14px', padding: '5px 12px', fontSize: '11px', fontWeight: '600', color: 'var(--text-secondary)', cursor: 'pointer' }}
                              >
                                "{chip}"
                              </button>
                            ))}
                          </div>
                        </div>

                      </div>

                      {/* RIGHT HERO COLUMN: ARTISAN & PRODUCT COLLAGE */}
                      <div className="hide-mobile" style={{ position: 'relative' }}>
                        <div style={{ height: '480px', borderRadius: '24px', overflow: 'hidden', boxShadow: '0 20px 40px rgba(0,0,0,0.12)' }}>
                          <img
                            src="https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=1000&q=80"
                            alt="Jaipur Terracotta Pottery"
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                          />
                        </div>

                        {/* FLOATING ARTISAN BADGE CARD */}
                        <div className="card-artisan" style={{ position: 'absolute', top: '24px', left: '-20px', padding: '16px 20px', display: 'flex', gap: '12px', alignItems: 'center', background: 'rgba(255,255,255,0.96)', backdropFilter: 'blur(8px)' }}>
                          <div style={{ width: '44px', height: '44px', borderRadius: '50%', background: 'var(--primary)', color: '#FFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '800', fontSize: '18px' }}>
                            🏺
                          </div>
                          <div>
                            <div style={{ fontSize: '14px', fontWeight: '800' }}>Ramswaroop Prajapat</div>
                            <div style={{ fontSize: '11px', color: 'var(--primary)', fontWeight: '700' }}>Master Potter • Jaipur, Rajasthan</div>
                          </div>
                        </div>

                        {/* FLOATING DIRECT PROCEEDS CARD */}
                        <div className="card-artisan" style={{ position: 'absolute', bottom: '24px', right: '-20px', padding: '16px 20px', background: 'rgba(255,255,255,0.96)', backdropFilter: 'blur(8px)' }}>
                          <div style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: '700' }}>FAIR TRADE COST TRANSPARENCY</div>
                          <div style={{ fontSize: '20px', fontWeight: '800', color: 'var(--text-main)', marginTop: '2px' }}>₹480 <span style={{ fontSize: '12px', color: '#10B981' }}>(100% Direct to Artisan)</span></div>
                        </div>
                      </div>

                    </div>
                  </div>
                </section>

                {/* 2. IMAGE-FOCUSED CATEGORIES SECTION */}
                <section style={{ padding: '80px 0', background: 'var(--bg-surface)', borderBottom: '1px solid var(--border-subtle)' }}>
                  <div className="container-wide">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '40px' }}>
                      <div>
                        <span className="badge-tag badge-gold" style={{ marginBottom: '8px' }}>Heritage Craftsmanship</span>
                        <h2 className="font-serif" style={{ fontSize: '32px', fontWeight: '700' }}>Explore By Craft Category</h2>
                      </div>
                      <button className="btn-artisan-outline" onClick={() => switchCustomerTab('shop')}>
                        View All Categories →
                      </button>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px' }}>
                      {[
                        { name: 'Pottery / Terracotta', count: '120+ Products', image: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=600&q=80' },
                        { name: 'Textiles / Handloom', count: '350+ Products', image: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=600&q=80' },
                        { name: 'Metal craft', count: '90+ Products', image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=600&q=80' },
                        { name: 'Woodwork', count: '140+ Products', image: 'https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=600&q=80' },
                        { name: 'Jewelry (traditional)', count: '210+ Products', image: 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=600&q=80' }
                      ].map(cat => (
                        <div
                          key={cat.name}
                          className="card-artisan"
                          onClick={() => {
                            setActiveCategoryFilter(cat.name);
                            switchCustomerTab('shop');
                          }}
                          style={{ cursor: 'pointer' }}
                        >
                          <div className="product-card-img-wrapper" style={{ height: '180px' }}>
                            <img src={cat.image} alt={cat.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                          </div>
                          <div style={{ padding: '16px', textAlign: 'center' }}>
                            <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)', marginBottom: '2px' }}>{cat.name}</h3>
                            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{cat.count}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </section>

                {/* 3. TRENDING PRODUCTS GRID (4 CARDS PER ROW DESKTOP) */}
                <section style={{ padding: '80px 0' }}>
                  <div className="container-wide">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '40px' }}>
                      <div>
                        <span className="badge-tag badge-terracotta" style={{ marginBottom: '8px' }}>Direct Market Linkage</span>
                        <h2 className="font-serif" style={{ fontSize: '32px', fontWeight: '700' }}>Trending Artisan Products</h2>
                      </div>
                      <button className="btn-artisan-outline" onClick={() => switchCustomerTab('shop')}>
                        Browse Shop Catalog →
                      </button>
                    </div>

                    <div className="desktop-grid-4">
                      {products.map(p => (
                        <div
                          key={p.id}
                          className="card-artisan"
                          onClick={() => setSelectedProduct(p)}
                          style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', cursor: 'pointer' }}
                        >
                          <div>
                            {/* PRODUCT IMAGE & WISHLIST */}
                            <div className="product-card-img-wrapper" style={{ height: '240px' }}>
                              <img src={p.image} alt={p.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                              
                              <button
                                onClick={(e) => toggleWishlist(p.id, e)}
                                style={{
                                  position: 'absolute',
                                  top: '12px',
                                  right: '12px',
                                  background: 'rgba(255,255,255,0.85)',
                                  backdropFilter: 'blur(4px)',
                                  border: 'none',
                                  width: '36px',
                                  height: '36px',
                                  borderRadius: '50%',
                                  display: 'flex',
                                  alignItems: 'center',
                                  justifyContent: 'center',
                                  cursor: 'pointer',
                                  zIndex: 2
                                }}
                              >
                                <Heart size={18} color={wishlist.includes(p.id) ? '#E11D48' : '#78716C'} fill={wishlist.includes(p.id) ? '#E11D48' : 'none'} />
                              </button>

                              <span className="badge-tag badge-terracotta" style={{ position: 'absolute', bottom: '12px', left: '12px', background: 'rgba(255,255,255,0.94)' }}>
                                {p.badge || 'Fair Trade'}
                              </span>
                            </div>

                            {/* CARD CONTENT */}
                            <div style={{ padding: '18px 18px 0' }}>
                              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', marginBottom: '6px' }}>
                                <span style={{ color: 'var(--primary)', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '3px' }}>
                                  <MapPin size={12} /> {p.artisan || 'Master Artisan'}
                                </span>
                                <span style={{ display: 'flex', alignItems: 'center', gap: '3px', fontWeight: '700', color: '#D97706' }}>
                                  <Star size={12} fill="#D97706" /> {p.rating || 4.9}
                                </span>
                              </div>

                              <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)', marginBottom: '8px', lineHeight: '1.35', height: '42px', overflow: 'hidden' }}>
                                {p.title}
                              </h3>
                            </div>
                          </div>

                          {/* PRICE & ADD TO CART */}
                          <div style={{ padding: '16px 18px 18px', borderTop: '1px solid var(--border-subtle)', marginTop: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                              <span style={{ fontSize: '20px', fontWeight: '800', color: 'var(--text-main)' }}>₹{p.price}</span>
                              {p.originalPrice && (
                                <span style={{ fontSize: '12px', color: 'var(--text-muted)', textDecoration: 'line-through', marginLeft: '6px' }}>₹{p.originalPrice}</span>
                              )}
                            </div>

                            <button
                              className="btn-artisan-primary"
                              onClick={(e) => addToCart(p, e)}
                              style={{ padding: '8px 14px', fontSize: '13px' }}
                            >
                              <ShoppingCart size={15} /> Add to Cart
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </section>

                {/* 4. HOW KAARVO WORKS SECTION */}
                <section style={{ padding: '80px 0', background: 'var(--bg-surface)', borderTop: '1px solid var(--border-subtle)', borderBottom: '1px solid var(--border-subtle)' }}>
                  <div className="container-wide">
                    <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 48px' }}>
                      <span className="badge-tag badge-gold" style={{ marginBottom: '8px' }}>Simple & Transparent</span>
                      <h2 className="font-serif" style={{ fontSize: '32px', fontWeight: '700' }}>How Kaarvo Works</h2>
                      <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: '8px' }}>
                        Empowering artisans through AI innovation and transparent ONDC market linkage.
                      </p>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '32px' }}>
                      {[
                        { step: '01', title: 'Discover Crafts', desc: 'Browse verified handcrafted products cataloged directly from artisan clusters across India.', icon: '🏺' },
                        { step: '02', title: 'Ask Kaarvo AI', desc: 'Use natural voice or search queries to find exact products tailored to your occasion and budget.', icon: '✨' },
                        { step: '03', title: 'Direct Purchase', desc: 'Orders are processed directly to the artisan via ONDC Beckn protocol with 100% fair trade proceeds.', icon: '📦' }
                      ].map(item => (
                        <div key={item.step} className="card-artisan" style={{ padding: '32px', textAlign: 'center' }}>
                          <div style={{ fontSize: '36px', marginBottom: '16px' }}>{item.icon}</div>
                          <span className="badge-tag badge-terracotta" style={{ marginBottom: '12px' }}>Step {item.step}</span>
                          <h3 style={{ fontSize: '20px', fontWeight: '800', marginBottom: '8px' }}>{item.title}</h3>
                          <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>{item.desc}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </section>

                {/* 5. FEATURED ARTISANS SECTION */}
                <section style={{ padding: '80px 0' }}>
                  <div className="container-wide">
                    <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 48px' }}>
                      <span className="badge-tag badge-terracotta" style={{ marginBottom: '8px' }}>Meet The Makers</span>
                      <h2 className="font-serif" style={{ fontSize: '32px', fontWeight: '700' }}>Master Indian Artisans</h2>
                      <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: '8px' }}>
                        Meet the heritage craftspeople keeping ancient Indian arts alive.
                      </p>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '28px' }}>
                      {[
                        {
                          name: 'Ramswaroop Prajapat',
                          craft: 'Master Terracotta Potter',
                          location: 'Jaipur, Rajasthan',
                          desc: '4th generation potter preserving eco-friendly clay water vessels with hand-carved relief motifs.',
                          image: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=500&q=80'
                        },
                        {
                          name: 'Sunita Devi Weaver Guild',
                          craft: 'Chanderi Silk Weaver',
                          location: 'Chanderi, Madhya Pradesh',
                          desc: 'Weaving regal Chanderi sarees on handloom frames with gold zari heritage peacock motifs.',
                          image: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=500&q=80'
                        },
                        {
                          name: 'Bishnu Jhara',
                          craft: 'Dhokra Metal Artisan',
                          location: 'Bastar, Chhattisgarh',
                          desc: 'Practicing 4,000-year-old lost-wax metal casting technique to create solid brass tribal figurines.',
                          image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=500&q=80'
                        }
                      ].map(artisan => (
                        <div key={artisan.name} className="card-artisan" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                          <div style={{ display: 'flex', gap: '16px', alignItems: 'center', marginBottom: '16px' }}>
                            <img src={artisan.image} alt={artisan.name} style={{ width: '80px', height: '80px', borderRadius: '50%', objectFit: 'cover' }} />
                            <div>
                              <span className="badge-tag badge-terracotta" style={{ fontSize: '10px', marginBottom: '4px' }}>Verified Artisan</span>
                              <h3 style={{ fontSize: '18px', fontWeight: '800' }}>{artisan.name}</h3>
                              <p style={{ fontSize: '13px', color: 'var(--primary)', fontWeight: '700' }}>{artisan.craft}</p>
                              <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>📍 {artisan.location}</p>
                            </div>
                          </div>
                          <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5', marginBottom: '20px' }}>{artisan.desc}</p>
                          <button className="btn-artisan-outline" onClick={() => switchCustomerTab('shop')} style={{ width: '100%' }}>
                            View Artisan Products →
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </section>

                {/* 6. DEDICATED PERSONAL CRAFT ASSISTANT SECTION */}
                <section style={{ padding: '80px 0', background: 'var(--primary-light)', borderTop: '1px solid var(--primary-border)', borderBottom: '1px solid var(--primary-border)' }}>
                  <div className="container-wide">
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '48px', alignItems: 'center' }}>
                      <div>
                        <span className="badge-tag badge-terracotta" style={{ marginBottom: '12px' }}>AI Shopping Innovation</span>
                        <h2 className="font-serif" style={{ fontSize: '36px', fontWeight: '700', marginBottom: '16px' }}>
                          Your Personal Craft Assistant
                        </h2>
                        <p style={{ fontSize: '16px', color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '24px' }}>
                          Ask Kaarvo AI anything using natural language voice or text. Get intelligent recommendations tailored to your exact budget, occasion, and style.
                        </p>
                        <button className="btn-artisan-primary" onClick={() => switchCustomerTab('ai_ask')} style={{ padding: '14px 28px' }}>
                          Try Ask Kaarvo AI →
                        </button>
                      </div>

                      <div className="card-artisan" style={{ padding: '24px', background: '#FFFFFF' }}>
                        <div style={{ fontSize: '13px', fontWeight: '800', color: 'var(--primary)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <Sparkles size={16} /> Live AI Shopping Query Demo
                        </div>
                        <div style={{ background: 'var(--bg-subtle)', padding: '14px', borderRadius: '12px', fontSize: '13px', color: 'var(--text-main)', marginBottom: '14px' }}>
                          "I need a traditional Jaipur gift under ₹1000 for a housewarming."
                        </div>
                        <div style={{ fontSize: '12px', color: '#10B981', fontWeight: '700', marginBottom: '8px' }}>
                          ✓ AI Recommended Product:
                        </div>
                        <div style={{ display: 'flex', gap: '12px', alignItems: 'center', background: 'var(--primary-light)', padding: '12px', borderRadius: '10px' }}>
                          <img src={products[0]?.image} alt="Pottery" style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '8px' }} />
                          <div>
                            <div style={{ fontSize: '13px', fontWeight: '700' }}>{products[0]?.title}</div>
                            <div style={{ fontSize: '14px', fontWeight: '800', color: 'var(--primary)' }}>₹{products[0]?.price}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>

                {/* 7. CRAFT STORIES SECTION */}
                <section style={{ padding: '80px 0', background: 'var(--bg-surface)' }}>
                  <div className="container-wide">
                    <div style={{ textAlign: 'center', maxWidth: '640px', margin: '0 auto 48px' }}>
                      <span className="badge-tag badge-gold" style={{ marginBottom: '8px' }}>Cultural Preservation</span>
                      <h2 className="font-serif" style={{ fontSize: '32px', fontWeight: '700' }}>Authentic Craft Stories</h2>
                      <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: '8px' }}>
                        The people and 4,000-year heritage behind every piece.
                      </p>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
                      {[
                        {
                          title: '4,000 Years of Dhokra Metal Casting',
                          artisan: 'Bishnu Jhara • Bastar, Chhattisgarh',
                          image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80',
                          content: 'Dhokra is one of the oldest non-ferrous metal casting techniques known to human civilization, dating back to the Indus Valley Dancing Girl figurine. Using beeswax thread sculpting and clay baking, each mold is broken open after cooling, making every single piece an irreplicable antique.'
                        },
                        {
                          title: 'Jaipur Natural Cooling Clay Pottery',
                          artisan: 'Ramswaroop Prajapat • Jaipur, Rajasthan',
                          image: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=80',
                          content: 'Crafted from rich alluvial Jaipur clay, these water pitchers utilize micro-porous capillary evaporation to naturally cool water down by 5-8°C without electricity or chemical filters.'
                        }
                      ].map((story, i) => (
                        <div key={i} className="card-artisan" style={{ padding: '28px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                          <img src={story.image} alt={story.title} style={{ width: '100%', height: '220px', objectFit: 'cover', borderRadius: '14px', marginBottom: '20px' }} />
                          <div>
                            <span className="badge-tag badge-terracotta" style={{ marginBottom: '8px' }}>{story.artisan}</span>
                            <h3 className="font-serif" style={{ fontSize: '22px', fontWeight: '700', marginBottom: '12px' }}>{story.title}</h3>
                            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>{story.content}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </section>

                {/* 8. STRONG FINAL PRE-FOOTER CTA */}
                <section style={{ padding: '80px 0', background: 'var(--bg-dark)', color: '#FFFFFF', textAlign: 'center' }}>
                  <div className="container-wide" style={{ maxWidth: '800px' }}>
                    <h2 className="font-serif" style={{ fontSize: '42px', fontWeight: '700', marginBottom: '16px' }}>
                      Discover something made differently.
                    </h2>
                    <p style={{ fontSize: '16px', color: '#A8A29E', lineHeight: '1.6', marginBottom: '32px' }}>
                      Support master Indian craftspeople directly with 100% transparent fair-trade pricing and verified heritage quality.
                    </p>
                    <button className="btn-artisan-primary" onClick={() => switchCustomerTab('shop')} style={{ padding: '16px 36px', fontSize: '16px' }}>
                      Explore Crafts Catalog <ArrowRight size={18} />
                    </button>
                  </div>
                </section>

                {/* FOOTER */}
                <footer style={{ background: '#141210', color: '#A8A29E', padding: '48px 0 24px', borderTop: '1px solid #292524' }}>
                  <div className="container-wide">
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '32px', marginBottom: '36px' }}>
                      <div>
                        <div style={{ fontSize: '22px', fontWeight: '800', color: '#FFF', marginBottom: '8px' }}>
                          Kaarvo<span style={{ color: 'var(--primary)' }}>.</span>
                        </div>
                        <p style={{ fontSize: '13px', lineHeight: '1.5', color: '#78716C' }}>
                          AI-Native Commerce Operating System empowering Indian craftspeople under MoSJE Smart India Hackathon initiative.
                        </p>
                      </div>

                      <div>
                        <h4 style={{ fontSize: '14px', fontWeight: '700', color: '#FFF', marginBottom: '12px' }}>Explore Crafts</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '13px' }}>
                          <span>Terracotta & Pottery</span>
                          <span>Handloom & Textiles</span>
                          <span>Dhokra Metal Art</span>
                          <span>Saharanpur Woodwork</span>
                        </div>
                      </div>

                      <div>
                        <h4 style={{ fontSize: '14px', fontWeight: '700', color: '#FFF', marginBottom: '12px' }}>Platform Standards</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '13px' }}>
                          <span>✓ ONDC Beckn Protocol</span>
                          <span>✓ Bhashini Multilingual Speech</span>
                          <span>✓ OpenCV Background Removal</span>
                          <span>✓ Transparent Cost-Plus Model</span>
                        </div>
                      </div>
                    </div>

                    <div style={{ borderTop: '1px solid #292524', paddingTop: '20px', textAlign: 'center', fontSize: '12px', color: '#78716C' }}>
                      © 2026 Kaarvo AI. Built for Smart India Hackathon SIH26090. All rights reserved.
                    </div>
                  </div>
                </footer>

              </div>
            )}

            {/* VIEW 2: CUSTOMER CATALOG / SHOP PAGE */}
            {customerTab === 'shop' && (
              <div className="container-wide" style={{ padding: '40px 28px 80px' }}>
                <div style={{ marginBottom: '32px' }}>
                  <h1 className="font-serif" style={{ fontSize: '36px', fontWeight: '700', marginBottom: '8px' }}>Explore Handcrafted Products</h1>
                  <p style={{ fontSize: '15px', color: 'var(--text-secondary)' }}>Direct market linkage connecting master artisans with customers nationwide.</p>
                </div>

                {/* SEARCH & FILTER CONTROLS */}
                <div className="card-artisan" style={{ padding: '16px 20px', marginBottom: '36px', display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
                  <div style={{ flex: 1, position: 'relative', minWidth: '260px' }}>
                    <Search size={18} color="var(--text-muted)" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)' }} />
                    <input
                      type="text"
                      className="input-artisan"
                      value={customerSearchQuery}
                      onChange={(e) => setCustomerSearchQuery(e.target.value)}
                      placeholder="Search by title, craft, material or artisan region..."
                      style={{ paddingLeft: '42px' }}
                    />
                  </div>

                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {['All', 'Pottery / Terracotta', 'Textiles / Handloom', 'Metal craft', 'Woodwork', 'Jewelry (traditional)'].map(cat => (
                      <button
                        key={cat}
                        onClick={() => setActiveCategoryFilter(cat)}
                        className={activeCategoryFilter === cat ? 'btn-artisan-primary' : 'btn-artisan-secondary'}
                        style={{ padding: '8px 14px', fontSize: '12px' }}
                      >
                        {cat}
                      </button>
                    ))}
                  </div>
                </div>

                {/* PRODUCTS 4-COLUMN DESKTOP GRID */}
                {filteredProducts.length === 0 ? (
                  <div className="card-artisan" style={{ padding: '60px 20px', textAlign: 'center' }}>
                    <Search size={48} color="var(--text-muted)" style={{ marginBottom: '12px' }} />
                    <h3 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '4px' }}>No Products Found</h3>
                    <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Try resetting your search query or category filters.</p>
                  </div>
                ) : (
                  <div className="desktop-grid-4">
                    {filteredProducts.map(p => (
                      <div
                        key={p.id}
                        className="card-artisan"
                        onClick={() => setSelectedProduct(p)}
                        style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', cursor: 'pointer' }}
                      >
                        <div>
                          <div className="product-card-img-wrapper" style={{ height: '240px' }}>
                            <img src={p.image} alt={p.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                            <span className="badge-tag badge-terracotta" style={{ position: 'absolute', bottom: '12px', left: '12px', background: 'rgba(255,255,255,0.94)' }}>
                              {p.category}
                            </span>
                          </div>

                          <div style={{ padding: '18px 18px 0' }}>
                            <div style={{ fontSize: '12px', color: 'var(--primary)', fontWeight: '600', marginBottom: '4px' }}>
                              📍 {p.artisan || 'Artisan Guild'} • {p.location || 'India'}
                            </div>

                            <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--text-main)', marginBottom: '8px', lineHeight: '1.35', height: '42px', overflow: 'hidden' }}>
                              {p.title}
                            </h3>
                          </div>
                        </div>

                        <div style={{ padding: '16px 18px 18px', borderTop: '1px solid var(--border-subtle)', marginTop: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <div>
                            <span style={{ fontSize: '20px', fontWeight: '800', color: 'var(--text-main)' }}>₹{p.price}</span>
                          </div>

                          <button
                            className="btn-artisan-primary"
                            onClick={(e) => addToCart(p, e)}
                            style={{ padding: '8px 14px', fontSize: '13px' }}
                          >
                            <ShoppingCart size={15} /> Add to Cart
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* VIEW 3: ASK KAARVO AI SHOPPING ASSISTANT */}
            {customerTab === 'ai_ask' && (
              <div className="container-wide" style={{ maxWidth: '960px', padding: '40px 28px 80px' }}>
                <div className="card-artisan" style={{ padding: '32px', marginBottom: '28px', background: 'linear-gradient(135deg, #FDF4EF, #F3F1E9)' }}>
                  <div style={{ display: 'flex', gap: '16px', alignItems: 'center', marginBottom: '14px' }}>
                    <div style={{ background: 'var(--primary)', color: '#FFF', padding: '12px', borderRadius: '14px' }}>
                      <Sparkles size={28} />
                    </div>
                    <div>
                      <h2 className="font-serif" style={{ fontSize: '28px', fontWeight: '700' }}>Ask Kaarvo AI Craft Assistant</h2>
                      <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '2px' }}>Get instant personalized recommendations directly from Indian master artisans.</p>
                    </div>
                  </div>

                  {/* QUICK SUGGESTIONS */}
                  <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '18px' }}>
                    {[
                      'Handmade gift under ₹1500',
                      'Traditional Indian crafts',
                      'Home decor',
                      'Wedding gifts'
                    ].map(prompt => (
                      <button
                        key={prompt}
                        onClick={() => handleAiShoppingQuery(prompt)}
                        className="btn-artisan-secondary"
                        style={{ fontSize: '13px', padding: '8px 16px' }}
                      >
                        💡 "{prompt}"
                      </button>
                    ))}
                  </div>
                </div>

                {/* CONVERSATION HISTORY */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '18px', marginBottom: '28px' }}>
                  {aiShoppingHistory.map((m, idx) => (
                    <div
                      key={idx}
                      className="card-artisan"
                      style={{
                        padding: '24px',
                        background: m.sender === 'user' ? 'var(--primary-light)' : 'var(--bg-surface)',
                        borderColor: m.sender === 'user' ? 'var(--primary-border)' : 'var(--border-subtle)'
                      }}
                    >
                      <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '8px', fontSize: '14px', fontWeight: '700', color: m.sender === 'user' ? 'var(--primary)' : 'var(--text-main)' }}>
                        {m.sender === 'user' ? '👤 You' : '🤖 Kaarvo AI Assistant'}
                      </div>

                      <p style={{ fontSize: '15px', color: 'var(--text-main)', lineHeight: '1.5', marginBottom: m.recommendedProducts ? '16px' : '0' }}>
                        {m.text}
                      </p>

                      {/* RECOMMENDED PRODUCTS CARDS */}
                      {m.recommendedProducts && (
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px', marginTop: '14px' }}>
                          {m.recommendedProducts.map(p => (
                            <div key={p.id} style={{ background: 'var(--bg-body)', padding: '14px', borderRadius: '14px', border: '1px solid var(--border-subtle)' }}>
                              <img src={p.image} alt={p.title} style={{ width: '100%', height: '140px', objectFit: 'cover', borderRadius: '10px', marginBottom: '10px' }} />
                              <div style={{ fontSize: '14px', fontWeight: '700', marginBottom: '4px' }}>{p.title}</div>
                              <div style={{ fontSize: '16px', fontWeight: '800', color: 'var(--primary)', marginBottom: '10px' }}>₹{p.price}</div>
                              <button className="btn-artisan-primary" onClick={(e) => addToCart(p, e)} style={{ width: '100%', padding: '8px', fontSize: '13px' }}>
                                Add to Cart
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}

                  {aiShoppingLoading && (
                    <div className="card-artisan" style={{ padding: '24px', textAlign: 'center', color: 'var(--primary)' }}>
                      <RefreshCw size={22} className="animate-spin" style={{ display: 'inline', marginRight: '8px' }} />
                      Kaarvo AI is searching verified artisan catalog...
                    </div>
                  )}
                </div>

                {/* AI INPUT BAR */}
                <div className="card-artisan" style={{ padding: '14px', display: 'flex', gap: '12px' }}>
                  <input
                    type="text"
                    className="input-artisan"
                    value={aiShoppingInput}
                    onChange={(e) => setAiShoppingInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAiShoppingQuery()}
                    placeholder="Ask Kaarvo AI anything e.g. 'Show me traditional Indian crafts under ₹2000'..."
                    style={{ border: 'none' }}
                  />
                  <button className="btn-artisan-primary" onClick={() => handleAiShoppingQuery()} style={{ padding: '12px 24px' }}>
                    <Send size={16} /> Ask
                  </button>
                </div>
              </div>
            )}

            {/* VIEW 4: CRAFT STORIES */}
            {customerTab === 'stories' && (
              <div className="container-wide" style={{ maxWidth: '1080px', padding: '40px 28px 80px' }}>
                <div style={{ marginBottom: '40px', textAlign: 'center' }}>
                  <span className="badge-tag badge-gold" style={{ marginBottom: '8px' }}>Cultural Preservation</span>
                  <h1 className="font-serif" style={{ fontSize: '38px', fontWeight: '700' }}>Heritage Craft Stories</h1>
                  <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: '8px' }}>
                    Discover the ancient techniques, regional traditions, and artisan families behind every piece.
                  </p>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '36px' }}>
                  {[
                    {
                      title: '4,000 Years of Dhokra Metal Casting',
                      artisan: 'Bishnu Jhara • Bastar, Chhattisgarh',
                      image: 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=1000&q=80',
                      content: 'Dhokra is one of the oldest non-ferrous metal casting techniques known to human civilization, dating back to the Indus Valley Dancing Girl figurine. Using beeswax thread sculpting and clay baking, each mold is broken open after cooling, making every single piece an irreplicable antique.'
                    },
                    {
                      title: 'Jaipur Natural Cooling Clay Pottery',
                      artisan: 'Ramswaroop Prajapat • Jaipur, Rajasthan',
                      image: 'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=1000&q=80',
                      content: 'Crafted from rich alluvial Jaipur clay, these water pitchers utilize micro-porous capillary evaporation to naturally cool water down by 5-8°C without electricity or chemical filters.'
                    }
                  ].map((story, i) => (
                    <div key={i} className="card-artisan" style={{ padding: '32px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px', alignItems: 'center' }}>
                      <img src={story.image} alt={story.title} style={{ width: '100%', height: '260px', objectFit: 'cover', borderRadius: '16px' }} />
                      <div>
                        <span className="badge-tag badge-terracotta" style={{ marginBottom: '10px' }}>{story.artisan}</span>
                        <h3 className="font-serif" style={{ fontSize: '24px', fontWeight: '700', marginBottom: '12px' }}>{story.title}</h3>
                        <p style={{ fontSize: '15px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>{story.content}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </main>

          {/* PRODUCT DETAIL MODAL / VIEW */}
          {selectedProduct && (
            <div className="modal-backdrop" onClick={() => setSelectedProduct(null)}>
              <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '860px' }}>
                <button
                  onClick={() => setSelectedProduct(null)}
                  style={{ position: 'absolute', top: '20px', right: '20px', background: 'var(--bg-subtle)', border: 'none', width: '36px', height: '36px', borderRadius: '50%', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                >
                  <X size={20} />
                </button>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px', alignItems: 'start' }}>
                  <img src={selectedProduct.image} alt={selectedProduct.title} style={{ width: '100%', height: '360px', objectFit: 'cover', borderRadius: '18px' }} />

                  <div>
                    <span className="badge-tag badge-terracotta" style={{ marginBottom: '10px' }}>{selectedProduct.category}</span>
                    <h2 style={{ fontSize: '24px', fontWeight: '800', marginBottom: '8px' }}>{selectedProduct.title}</h2>
                    
                    <div style={{ fontSize: '14px', color: 'var(--primary)', fontWeight: '600', marginBottom: '14px' }}>
                      📍 Artisan: {selectedProduct.artisan || 'Master Artisan Guild'} • {selectedProduct.location || 'India'}
                    </div>

                    <div style={{ fontSize: '28px', fontWeight: '800', color: 'var(--text-main)', marginBottom: '18px' }}>
                      ₹{selectedProduct.price}
                    </div>

                    <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '20px' }}>
                      {selectedProduct.description}
                    </p>

                    <div style={{ background: 'var(--bg-subtle)', padding: '14px', borderRadius: '12px', fontSize: '13px', marginBottom: '24px' }}>
                      <div style={{ fontWeight: '700', marginBottom: '4px' }}>✨ Fair Trade Cost Breakdown</div>
                      <div style={{ color: 'var(--text-muted)' }}>Material: ₹180 | Artisan Labor: ₹150 | Fair Margin: 40%</div>
                    </div>

                    <div style={{ display: 'flex', gap: '12px' }}>
                      <button
                        className="btn-artisan-primary"
                        onClick={(e) => {
                          addToCart(selectedProduct, e);
                          setSelectedProduct(null);
                        }}
                        style={{ flex: 1, padding: '14px' }}
                      >
                        <ShoppingCart size={18} /> Add to Cart
                      </button>
                      <button
                        className="btn-artisan-secondary"
                        onClick={(e) => {
                          addToCart(selectedProduct, e);
                          setSelectedProduct(null);
                          setIsCartOpen(true);
                        }}
                        style={{ flex: 1, padding: '14px' }}
                      >
                        Buy Now
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* CART DRAWER & CHECKOUT */}
          {isCartOpen && (
            <div className="modal-backdrop" onClick={() => setIsCartOpen(false)}>
              <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '500px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                  <h3 style={{ fontSize: '20px', fontWeight: '800' }}>Your Shopping Cart ({cartItems.length})</h3>
                  <button onClick={() => setIsCartOpen(false)} style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}>
                    <X size={22} />
                  </button>
                </div>

                {cartItems.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '48px 0', color: 'var(--text-muted)' }}>
                    <ShoppingCart size={54} style={{ marginBottom: '16px' }} />
                    <p style={{ fontSize: '15px' }}>Your cart is empty.</p>
                  </div>
                ) : (
                  <div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', maxHeight: '320px', overflowY: 'auto', marginBottom: '24px' }}>
                      {cartItems.map(item => (
                        <div key={item.id} style={{ display: 'flex', gap: '14px', alignItems: 'center', background: 'var(--bg-subtle)', padding: '12px', borderRadius: '12px' }}>
                          <img src={item.image} alt={item.title} style={{ width: '56px', height: '56px', objectFit: 'cover', borderRadius: '10px' }} />
                          <div style={{ flex: 1 }}>
                            <div style={{ fontSize: '14px', fontWeight: '700' }}>{item.title}</div>
                            <div style={{ fontSize: '15px', color: 'var(--primary)', fontWeight: '800' }}>₹{item.price}</div>
                          </div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <button onClick={() => updateCartQty(item.id, -1)} style={{ width: '28px', height: '28px', borderRadius: '6px', border: '1px solid var(--border-subtle)', cursor: 'pointer' }}>-</button>
                            <span style={{ fontSize: '14px', fontWeight: '700' }}>{item.quantity}</span>
                            <button onClick={() => updateCartQty(item.id, 1)} style={{ width: '28px', height: '28px', borderRadius: '6px', border: '1px solid var(--border-subtle)', cursor: 'pointer' }}>+</button>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '16px', marginBottom: '24px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '8px' }}>
                        <span>Subtotal</span>
                        <span>₹{cartSubtotal}</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '8px' }}>
                        <span>Delivery</span>
                        <span>{shippingFee === 0 ? 'FREE' : `₹${shippingFee}`}</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '20px', fontWeight: '800', color: 'var(--text-main)', marginTop: '10px' }}>
                        <span>Total</span>
                        <span>₹{cartTotal}</span>
                      </div>
                    </div>

                    <button
                      className="btn-artisan-primary"
                      onClick={() => {
                        setIsCartOpen(false);
                        setIsCheckoutOpen(true);
                      }}
                      style={{ width: '100%', padding: '16px', fontSize: '16px' }}
                    >
                      Proceed to Checkout →
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* CHECKOUT MODAL WITH PROGRESS INDICATOR */}
          {isCheckoutOpen && (
            <div className="modal-backdrop" onClick={() => setIsCheckoutOpen(false)}>
              <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '540px' }}>
                
                {/* PROGRESS INDICATOR */}
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '28px', position: 'relative' }}>
                  {['Address', 'Delivery', 'Payment', 'Confirmation'].map((stepName, i) => (
                    <div key={stepName} style={{ textAlign: 'center', flex: 1 }}>
                      <div style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '50%',
                        background: checkoutStep >= (i + 1) ? 'var(--primary)' : 'var(--bg-subtle)',
                        color: checkoutStep >= (i + 1) ? '#FFF' : 'var(--text-muted)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: '700',
                        fontSize: '13px',
                        margin: '0 auto 6px'
                      }}>
                        {i + 1}
                      </div>
                      <span style={{ fontSize: '12px', fontWeight: '600', color: checkoutStep >= (i + 1) ? 'var(--primary)' : 'var(--text-muted)' }}>
                        {stepName}
                      </span>
                    </div>
                  ))}
                </div>

                {/* STEP 1: ADDRESS */}
                {checkoutStep === 1 && (
                  <div>
                    <h3 style={{ fontSize: '20px', fontWeight: '800', marginBottom: '18px' }}>Shipping Address</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '24px' }}>
                      <input type="text" className="input-artisan" value={checkoutData.name} onChange={(e) => setCheckoutData({ ...checkoutData, name: e.target.value })} placeholder="Full Name" />
                      <input type="text" className="input-artisan" value={checkoutData.phone} onChange={(e) => setCheckoutData({ ...checkoutData, phone: e.target.value })} placeholder="Mobile Number" />
                      <input type="text" className="input-artisan" value={checkoutData.address} onChange={(e) => setCheckoutData({ ...checkoutData, address: e.target.value })} placeholder="Street Address" />
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                        <input type="text" className="input-artisan" value={checkoutData.city} onChange={(e) => setCheckoutData({ ...checkoutData, city: e.target.value })} placeholder="City" />
                        <input type="text" className="input-artisan" value={checkoutData.pincode} onChange={(e) => setCheckoutData({ ...checkoutData, pincode: e.target.value })} placeholder="Pincode" />
                      </div>
                    </div>
                    <button className="btn-artisan-primary" onClick={() => setCheckoutStep(2)} style={{ width: '100%', padding: '14px' }}>
                      Continue to Delivery →
                    </button>
                  </div>
                )}

                {/* STEP 2: DELIVERY */}
                {checkoutStep === 2 && (
                  <div>
                    <h3 style={{ fontSize: '20px', fontWeight: '800', marginBottom: '18px' }}>Delivery Option</h3>
                    <div style={{ background: 'var(--primary-light)', border: '1px solid var(--primary-border)', padding: '20px', borderRadius: '14px', marginBottom: '24px' }}>
                      <div style={{ fontWeight: '700', color: 'var(--primary)', fontSize: '15px' }}>🚀 Standard Direct Artisan Shipping</div>
                      <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '6px' }}>Dispatched directly from artisan studio in Jaipur. Estimated 3-5 business days.</div>
                    </div>
                    <div style={{ display: 'flex', gap: '12px' }}>
                      <button className="btn-artisan-secondary" onClick={() => setCheckoutStep(1)} style={{ padding: '14px 20px' }}>Back</button>
                      <button className="btn-artisan-primary" onClick={() => setCheckoutStep(3)} style={{ flex: 1, padding: '14px' }}>Continue to Payment →</button>
                    </div>
                  </div>
                )}

                {/* STEP 3: PAYMENT */}
                {checkoutStep === 3 && (
                  <div>
                    <h3 style={{ fontSize: '20px', fontWeight: '800', marginBottom: '18px' }}>Payment Method</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
                      {['UPI (PhonePe / GPay)', 'Cash on Delivery', 'Credit / Debit Card'].map(pm => (
                        <div
                          key={pm}
                          onClick={() => setCheckoutData({ ...checkoutData, paymentMethod: pm })}
                          style={{
                            padding: '16px',
                            borderRadius: '12px',
                            border: checkoutData.paymentMethod === pm ? '2px solid var(--primary)' : '1px solid var(--border-subtle)',
                            background: checkoutData.paymentMethod === pm ? 'var(--primary-light)' : 'var(--bg-surface)',
                            cursor: 'pointer',
                            fontWeight: '600',
                            fontSize: '15px'
                          }}
                        >
                          {pm}
                        </div>
                      ))}
                    </div>
                    <button className="btn-artisan-primary" onClick={handlePlaceOrder} disabled={isPlacingOrder} style={{ width: '100%', padding: '16px', fontSize: '16px' }}>
                      {isPlacingOrder ? 'Processing...' : `Confirm & Pay ₹${cartTotal}`}
                    </button>
                  </div>
                )}

                {/* STEP 4: SUCCESS */}
                {checkoutStep === 4 && (
                  <div style={{ textAlign: 'center', padding: '24px 0' }}>
                    <CheckCircle size={64} color="#10B981" style={{ marginBottom: '16px' }} />
                    <h2 style={{ fontSize: '26px', fontWeight: '800', marginBottom: '8px' }}>Order Placed Successfully!</h2>
                    <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '28px' }}>
                      Order notification sent directly to the artisan's ONDC Beckn Gateway.
                    </p>
                    <button className="btn-artisan-primary" onClick={() => setIsCheckoutOpen(false)} style={{ padding: '14px 28px' }}>
                      Return to Marketplace
                    </button>
                  </div>
                )}

              </div>
            </div>
          )}
        </>
      )}

      {/* ========================================================================= */}
      {/* MODE 2: ARTISAN BUSINESS OS & 3-PILLAR CATALOGER                           */}
      {/* ========================================================================= */}
      {mode === 'artisan' && (
        <div style={{ display: 'flex', flex: 1, minHeight: 'calc(100vh - 35px)' }}>
          
          {/* ARTISAN SIDEBAR NAVIGATION */}
          <aside style={{
            width: '270px',
            background: 'var(--bg-surface)',
            borderRight: '1px solid var(--border-subtle)',
            padding: '28px 18px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
            <div>
              {/* SIDEBAR HEADER */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '0 8px 24px', borderBottom: '1px solid var(--border-subtle)', marginBottom: '24px' }}>
                <div style={{ width: '38px', height: '38px', borderRadius: '10px', background: 'var(--primary)', color: '#FFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '800' }}>
                  🎨
                </div>
                <div>
                  <div style={{ fontWeight: '800', fontSize: '16px' }}>Artisan Business OS</div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>MoSJE SIH26090 Platform</div>
                </div>
              </div>

              {/* NAVIGATION LINKS */}
              <nav style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {[
                  { id: 'dashboard', label: 'Dashboard Overview', icon: Layers },
                  { id: 'studio', label: '✨ 3-Pillar AI Studio', icon: Sparkles },
                  { id: 'copilot', label: '🤖 AI Business Copilot', icon: Mic },
                  { id: 'orders', label: '🛒 Customer Orders', icon: ShoppingBag },
                  { id: 'customers', label: '👥 Customer 360', icon: Users },
                  { id: 'insights', label: '📈 Analytics & Profit', icon: PieChart },
                  { id: 'marketing', label: '📣 Social Campaigns', icon: Zap },
                  { id: 'settings', label: '⚙️ Business Settings', icon: Settings }
                ].map(item => {
                  const Icon = item.icon;
                  const isActive = artisanTab === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => switchArtisanTab(item.id)}
                      style={{
                        background: isActive ? 'var(--primary-light)' : 'transparent',
                        color: isActive ? 'var(--primary)' : 'var(--text-secondary)',
                        border: 'none',
                        padding: '12px 16px',
                        borderRadius: 'var(--radius-md)',
                        fontSize: '14px',
                        fontWeight: isActive ? '700' : '500',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        textAlign: 'left',
                        transition: 'all 0.2s ease'
                      }}
                    >
                      <Icon size={18} color={isActive ? 'var(--primary)' : 'var(--text-muted)'} />
                      {item.label}
                    </button>
                  );
                })}
              </nav>
            </div>

            {/* SWITCH BACK TO MARKETPLACE */}
            <button
              className="btn-artisan-secondary"
              onClick={() => switchMode('customer')}
              style={{ width: '100%', fontSize: '13px', padding: '12px' }}
            >
              ← Back to Customer Store
            </button>
          </aside>

          {/* MAIN ARTISAN OS BODY */}
          <main style={{ flex: 1, padding: '36px', maxWidth: '1280px', margin: '0 auto' }}>

            {/* ARTISAN VIEW 1: DASHBOARD OVERVIEW */}
            {artisanTab === 'dashboard' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
                
                {/* HERO STATS GRID */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px' }}>
                  <div className="card-artisan" style={{ padding: '24px' }}>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>Published Products</div>
                    <div style={{ fontSize: '32px', fontWeight: '800', color: 'var(--text-main)' }}>{products.length}</div>
                    <span className="badge-tag badge-teal" style={{ marginTop: '8px' }}>✓ ONDC Beckn Live</span>
                  </div>

                  <div className="card-artisan" style={{ padding: '24px' }}>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>Total Customer Orders</div>
                    <div style={{ fontSize: '32px', fontWeight: '800', color: 'var(--primary)' }}>{orders.length}</div>
                    <span className="badge-tag badge-terracotta" style={{ marginTop: '8px' }}>✓ Real-time Sync</span>
                  </div>

                  <div className="card-artisan" style={{ padding: '24px' }}>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>Artisan Revenue</div>
                    <div style={{ fontSize: '32px', fontWeight: '800', color: '#10B981' }}>
                      ₹{orders.reduce((s, o) => s + (parseFloat(o.total_price) || 0), 0) || 1850}
                    </div>
                    <span className="badge-tag badge-gold" style={{ marginTop: '8px' }}>✓ Direct Bank Transfer</span>
                  </div>

                  <div className="card-artisan" style={{ padding: '24px' }}>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '4px' }}>Quality Audit Score</div>
                    <div style={{ fontSize: '32px', fontWeight: '800', color: '#D97706' }}>98/100</div>
                    <span className="badge-tag badge-gold" style={{ marginTop: '8px' }}>✓ MoSJE Certified</span>
                  </div>
                </div>

                {/* AI INSIGHTS & ATTENTION REQUIRED */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
                  <div className="card-artisan" style={{ padding: '28px', background: 'var(--primary-light)', borderColor: 'var(--primary-border)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)', fontWeight: '700', marginBottom: '8px' }}>
                      <Sparkles size={18} /> AI Business Opportunity
                    </div>
                    <h4 style={{ fontSize: '18px', fontWeight: '800', marginBottom: '6px' }}>Diwali Demand Spike Detected</h4>
                    <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.5', marginBottom: '16px' }}>
                      Demand for handcrafted terracotta jugs in Rajasthan & Delhi is up 34%. Recommended: Use Cost-Plus Assistant to launch a 5% promotional bundle.
                    </p>
                    <button className="btn-artisan-primary" onClick={() => switchArtisanTab('studio')} style={{ padding: '8px 18px', fontSize: '13px' }}>
                      + Open 3-Pillar AI Studio
                    </button>
                  </div>

                  <div className="card-artisan" style={{ padding: '28px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#D97706', fontWeight: '700', marginBottom: '8px' }}>
                      <ShieldAlert size={18} /> Attention Required
                    </div>
                    <h4 style={{ fontSize: '18px', fontWeight: '800', marginBottom: '6px' }}>Pending Shipping Pickup</h4>
                    <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.5', marginBottom: '16px' }}>
                      Order #ORD-1045 requires packaging dispatch label print for courier pickup in Jaipur.
                    </p>
                    <button className="btn-artisan-secondary" onClick={() => switchArtisanTab('orders')} style={{ padding: '8px 18px', fontSize: '13px' }}>
                      View Orders →
                    </button>
                  </div>
                </div>

                {/* RECENT ORDERS TABLE */}
                <div className="card-artisan" style={{ padding: '28px' }}>
                  <h3 style={{ fontSize: '20px', fontWeight: '800', marginBottom: '18px' }}>Recent Order Activity</h3>
                  {orders.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-muted)', fontSize: '14px' }}>
                      No order activity yet.
                    </div>
                  ) : (
                    <table style={{ width: '100%', fontSize: '14px', borderCollapse: 'collapse' }}>
                      <thead>
                        <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                          <th style={{ padding: '12px', textAlign: 'left' }}>Order ID</th>
                          <th style={{ padding: '12px', textAlign: 'left' }}>Customer</th>
                          <th style={{ padding: '12px', textAlign: 'left' }}>Amount</th>
                          <th style={{ padding: '12px', textAlign: 'left' }}>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {orders.map((o, i) => (
                          <tr key={i} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                            <td style={{ padding: '12px', fontWeight: '700', color: 'var(--primary)' }}>ORD-{i + 1}</td>
                            <td style={{ padding: '12px' }}>{o.customer_name}</td>
                            <td style={{ padding: '12px', fontWeight: '800' }}>₹{o.total_price}</td>
                            <td style={{ padding: '12px' }}><span className="badge-tag badge-teal">Paid</span></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>

              </div>
            )}

            {/* ARTISAN VIEW 2: 3-PILLAR AI STUDIO (SIH26090 CORE SOLUTION) */}
            {artisanTab === 'studio' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
                <div>
                  <span className="badge-tag badge-terracotta" style={{ marginBottom: '6px' }}>SIH26090 Core Solution</span>
                  <h1 className="font-serif" style={{ fontSize: '32px', fontWeight: '700' }}>3-Pillar Smart Cataloger Studio</h1>
                  <p style={{ fontSize: '15px', color: 'var(--text-secondary)' }}>Turn phone photos & regional voice notes into studio catalog & ONDC Beckn schema.</p>
                </div>

                {/* 3 PILLARS GRID */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '28px' }}>
                  
                  {/* PILLAR 1 */}
                  <div className="card-artisan" style={{ padding: '28px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '18px' }}>
                      <Camera size={22} color="var(--primary)" />
                      <h3 style={{ fontSize: '18px', fontWeight: '700' }}>Pillar 1: AI Studio Image Enhancer</h3>
                    </div>

                    <label style={{ border: '2px dashed var(--border-strong)', padding: '28px', borderRadius: '14px', display: 'block', textAlign: 'center', cursor: 'pointer', background: 'var(--bg-subtle)', marginBottom: '16px' }}>
                      <input type="file" accept="image/*" onChange={handleEnhanceImage} style={{ display: 'none' }} />
                      <Camera size={36} color="var(--text-muted)" style={{ marginBottom: '10px' }} />
                      <div style={{ fontSize: '14px', fontWeight: '700' }}>Upload Raw Artisan Photo</div>
                      <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>Auto-removes background & balances lighting</div>
                    </label>

                    {imageEnhancing && (
                      <div style={{ textAlign: 'center', color: 'var(--primary)', fontSize: '13px' }}>
                        <RefreshCw size={18} className="animate-spin" style={{ display: 'inline', marginRight: '6px' }} />
                        Processing OpenCV Studio Enhancer...
                      </div>
                    )}

                    {enhancedImage && !imageEnhancing && (
                      <img src={enhancedImage} alt="Enhanced Studio" style={{ width: '100%', height: '180px', objectFit: 'cover', borderRadius: '12px' }} />
                    )}
                  </div>

                  {/* PILLAR 2 */}
                  <div className="card-artisan" style={{ padding: '28px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '18px' }}>
                      <Mic size={22} color="var(--primary)" />
                      <h3 style={{ fontSize: '18px', fontWeight: '700' }}>Pillar 2: Multilingual Voice Cataloger</h3>
                    </div>

                    <div style={{ display: 'flex', gap: '10px', marginBottom: '14px' }}>
                      <select value={selectedLanguage} onChange={(e) => setSelectedLanguage(e.target.value)} className="input-artisan" style={{ flex: 1 }}>
                        <option value="hi-IN">🇮🇳 Hindi (हिंदी)</option>
                        <option value="bn-IN">🇮🇳 Bengali (বাংলা)</option>
                        <option value="ta-IN">🇮🇳 Tamil (தமிழ்)</option>
                      </select>
                      <button className="btn-artisan-secondary" onClick={() => setIsRecording(!isRecording)}>
                        {isRecording ? 'Listening...' : 'Record'}
                      </button>
                    </div>

                    <textarea
                      rows={3}
                      className="input-artisan"
                      value={voiceText}
                      onChange={(e) => setVoiceText(e.target.value)}
                      style={{ resize: 'none', marginBottom: '14px' }}
                    />

                    <button className="btn-artisan-primary" onClick={handleGenerateCatalogFromVoice} disabled={cataloging} style={{ width: '100%', padding: '12px' }}>
                      {cataloging ? 'Processing Bhashini Speech...' : 'Generate Auto-Catalog'}
                    </button>
                  </div>

                  {/* PILLAR 3 */}
                  <div className="card-artisan" style={{ padding: '28px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '18px' }}>
                      <Sliders size={22} color="var(--primary)" />
                      <h3 style={{ fontSize: '18px', fontWeight: '700' }}>Pillar 3: Cost-Plus Pricing Engine</h3>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '16px' }}>
                      <div>
                        <label style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Material Cost (₹)</label>
                        <input type="number" className="input-artisan" value={materialCost} onChange={(e) => { setMaterialCost(e.target.value); calculatePricing(e.target.value, laborCost, craftCategory); }} />
                      </div>
                      <div>
                        <label style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Labor Cost (₹)</label>
                        <input type="number" className="input-artisan" value={laborCost} onChange={(e) => { setLaborCost(e.target.value); calculatePricing(materialCost, e.target.value, craftCategory); }} />
                      </div>
                    </div>

                    {pricingResult && (
                      <div style={{ background: 'var(--primary-light)', border: '1px solid var(--primary-border)', padding: '14px', borderRadius: '12px' }}>
                        <div style={{ fontSize: '20px', fontWeight: '800', color: 'var(--primary)' }}>
                          Suggested: ₹{pricingResult.min} – ₹{pricingResult.max}
                        </div>
                      </div>
                    )}
                  </div>

                </div>

                {/* GENERATED CATALOG PREVIEW & PUBLISH */}
                {generatedCatalog && (
                  <div className="card-artisan" style={{ padding: '32px', background: 'linear-gradient(135deg, #FDF4EF, #FFFFFF)', border: '1px solid var(--primary-border)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                      <span className="badge-tag badge-terracotta">✓ ONDC Beckn Schema Compliant</span>
                      <button className="btn-artisan-primary" onClick={handleSaveCatalogToDB} style={{ padding: '12px 24px' }}>
                        Save & Publish Live to Kaarvo Store →
                      </button>
                    </div>
                    <h3 style={{ fontSize: '22px', fontWeight: '800', marginBottom: '8px' }}>{generatedCatalog.descriptor.name}</h3>
                    <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>{generatedCatalog.descriptor.long_desc}</p>
                  </div>
                )}
              </div>
            )}

            {/* ARTISAN VIEW 3: AI BUSINESS COPILOT */}
            {artisanTab === 'copilot' && (
              <div style={{ maxWidth: '960px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '28px' }}>
                <div className="card-artisan" style={{ padding: '32px', background: 'var(--primary-light)', borderColor: 'var(--primary-border)' }}>
                  <h2 className="font-serif" style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}>How can I help your business today?</h2>
                  <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '20px' }}>Ask Kaarvo Copilot about sales analytics, pricing strategy, inventory or campaigns.</p>

                  <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                    {['+ Create Product', '📊 Analyze Sales', '🏷️ Suggest Price', '📣 Create Campaign', '📦 Check Inventory'].map(act => (
                      <button key={act} onClick={() => handleCopilotSend(act)} className="btn-artisan-secondary" style={{ fontSize: '13px', padding: '8px 16px' }}>
                        {act}
                      </button>
                    ))}
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  {copilotHistory.map((m, i) => (
                    <div key={i} className="card-artisan" style={{ padding: '24px', background: m.sender === 'artisan' ? 'var(--bg-subtle)' : 'var(--bg-surface)' }}>
                      <div style={{ fontSize: '13px', fontWeight: '700', color: m.sender === 'artisan' ? 'var(--text-muted)' : 'var(--primary)', marginBottom: '8px' }}>
                        {m.sender === 'artisan' ? '👤 Artisan' : '🤖 Kaarvo Copilot'}
                      </div>
                      <p style={{ fontSize: '15px', lineHeight: '1.6' }}>{m.content}</p>
                    </div>
                  ))}
                </div>

                <div className="card-artisan" style={{ padding: '14px', display: 'flex', gap: '12px' }}>
                  <input
                    type="text"
                    className="input-artisan"
                    value={copilotInput}
                    onChange={(e) => setCopilotInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleCopilotSend()}
                    placeholder="Ask Kaarvo anything about your craft business..."
                    style={{ border: 'none' }}
                  />
                  <button className="btn-artisan-primary" onClick={() => handleCopilotSend()} style={{ padding: '12px 24px' }}>
                    <Send size={16} /> Send
                  </button>
                </div>
              </div>
            )}

            {/* ARTISAN VIEW 4: ORDERS */}
            {artisanTab === 'orders' && (
              <div className="card-artisan" style={{ padding: '32px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: '800', marginBottom: '20px' }}>Customer Orders Dashboard</h2>
                {orders.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '48px 0', color: 'var(--text-muted)' }}>No customer orders found.</div>
                ) : (
                  <table style={{ width: '100%', fontSize: '14px', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                        <th style={{ padding: '12px', textAlign: 'left' }}>Order ID</th>
                        <th style={{ padding: '12px', textAlign: 'left' }}>Customer</th>
                        <th style={{ padding: '12px', textAlign: 'left' }}>Shipping Address</th>
                        <th style={{ padding: '12px', textAlign: 'left' }}>Total Amount</th>
                        <th style={{ padding: '12px', textAlign: 'left' }}>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {orders.map((o, idx) => (
                        <tr key={idx} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                          <td style={{ padding: '12px', fontWeight: '700', color: 'var(--primary)' }}>ORD-{idx + 1}</td>
                          <td style={{ padding: '12px', fontWeight: '600' }}>{o.customer_name}</td>
                          <td style={{ padding: '12px', color: 'var(--text-secondary)' }}>{o.shipping_address || 'Jaipur, Rajasthan'}</td>
                          <td style={{ padding: '12px', fontWeight: '800', color: '#10B981' }}>₹{o.total_price}</td>
                          <td style={{ padding: '12px' }}><span className="badge-tag badge-teal">Paid</span></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}

            {/* ARTISAN VIEW 5: CUSTOMERS / INSIGHTS / MARKETING / SETTINGS STUBS */}
            {['customers', 'insights', 'marketing', 'settings'].includes(artisanTab) && (
              <div className="card-artisan" style={{ padding: '60px', textAlign: 'center' }}>
                <div style={{ fontSize: '40px', marginBottom: '16px' }}>📊</div>
                <h2 style={{ fontSize: '24px', fontWeight: '800', marginBottom: '8px', textTransform: 'capitalize' }}>
                  {artisanTab} Module Active
                </h2>
                <p style={{ fontSize: '15px', color: 'var(--text-muted)' }}>
                  Integrated with Kaarvo Master AI Loop & ONDC Beckn Network.
                </p>
              </div>
            )}

          </main>
        </div>
      )}

    </div>
  );
}

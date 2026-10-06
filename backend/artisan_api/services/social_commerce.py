from artisan_api.models import Product

class SocialCommerceService:
    def generate_social_content(self, product: Product) -> dict:
        title = product.title
        desc = product.description
        price = product.price
        category = product.category

        whatsapp_copy = (
            f"🌺 *{title}* 🌺\n\n"
            f"{desc[:180]}...\n\n"
            f"💰 *Price:* ₹{price} (Direct from Artisan)\n"
            f"📦 *Shipping:* Pan-India Available\n"
            f"🛍️ *Order Now / View Craft Details:* https://artisan.in/store/{product.id}\n\n"
            f"#HandmadeIndia #VocalForLocal #{category.replace(' ', '')}"
        )

        instagram_caption = (
            f"✨ Authentic Artisan Creation ✨\n\n"
            f"{title}\n\n"
            f"{desc}\n\n"
            f"🏷️ Price: ₹{price}\n"
            f"👇 Tap link in bio to order directly and support local weavers & craftsmen!\n\n"
            f"#IndianArtisans #HandicraftIndia #VocalForLocal #ArtisanMade #EthicalShopping #Handloom #MadeInIndia"
        )

        return {
            'whatsapp_copy': whatsapp_copy,
            'instagram_caption': instagram_caption,
            'shareable_link': f"https://artisan.in/store/{product.id}"
        }

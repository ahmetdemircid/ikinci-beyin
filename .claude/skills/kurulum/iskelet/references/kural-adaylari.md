# Kural adayları (onay bekler, onaysız uygulanmaz)

Oturum kapanınca arka plandaki özetçi, kullanıcının "bundan sonra", "her zaman", "asla" gibi
söylediği yerleri buraya aday olarak yazar. `/gunu-ac` bekleyenleri gösterir. Onaylanan aday
`hafiza/otomatik/` altına kural olarak yazılır ve satırı `(durum: onaylandı)` olur; reddedilen
`(durum: reddedildi)` olur. Satır silinmez.

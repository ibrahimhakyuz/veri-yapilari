class Yolcu:
    def __init__(self, ad, soyad):
        self.ad = ad
        self.soyad = soyad

    def __str__(self):
        return "{} {}".format(self.ad, self.soyad)


class OtobusNode:
    def __init__(self, tarih, numara):
        self.tarih = tarih  
        self.numara = numara  
        self.yolcular = [] 
        self.left = None  # Erken tarihliler
        self.right = None  # Geç tarihliler

    def YolcuEkle(self, yolcu):
        self.yolcular.append(yolcu)

    def YolcuSil(self, yolcu_ad, yolcu_soyad):
        for yolcu in self.yolcular:
            if yolcu.ad == yolcu_ad and yolcu.soyad == yolcu_soyad:
                self.yolcular.remove(yolcu)
                return True
        return False

    def YolcuGuncelle(self, yolcu_ad, yolcu_soyad, yeni_ad, yeni_soyad):
        for yolcu in self.yolcular:
            if yolcu.ad == yolcu_ad and yolcu.soyad == yolcu_soyad:
                yolcu.ad = yeni_ad
                yolcu.soyad = yeni_soyad
                return True
        return False

    def __str__(self):
        yolcu_listesi = ', '.join([str(yolcu) for yolcu in self.yolcular])
        return "Otobüs No: {}, Tarih: {}, Yolcular: {}".format(self.numara, self.tarih, yolcu_listesi)


class OtobusYonetimSistemi:
    def __init__(self):
        self.root = None  #(root)

    def otobus_ekle(self, tarih, numara):
        if self.root is None:
            self.root = OtobusNode(tarih, numara)
        else:
            self._otobus_ekle(self.root, tarih, numara)

    def _otobus_ekle(self, node, tarih, numara):
        if tarih < node.tarih:  # Sol alt düğüme gitmek için (erken tarihli)
            if node.left is None:
                node.left = OtobusNode(tarih, numara)
            else:
                self._otobus_ekle(node.left, tarih, numara)
        elif tarih > node.tarih:  # Sağ alt düğüme gitmek için (geç tarihli)
            if node.right is None:
                node.right = OtobusNode(tarih, numara)
            else:
                self._otobus_ekle(node.right, tarih, numara)
        else:
            # numara ile kontrol
            current_node = node
            while current_node: 
                if current_node.numara == numara:
                    print("Bu tarihte ({}) {} numaralı bir otobüs zaten var.".format(tarih,numara))
                    return
                if numara < current_node.numara:
                    if current_node.left is None:
                        current_node.left = OtobusNode(tarih, numara)
                        return
                    current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = OtobusNode(tarih, numara)
                        return
                    current_node = current_node.right

    def yolcu_ekle(self, tarih, numara, yolcu):
        otobus_node = self.OtobusBul(self.root, tarih, numara)
        if otobus_node:
            otobus_node.YolcuEkle(yolcu)
            return "Yolcu {} başarılı bir şekilde otobüse eklendi.".format(yolcu)
        return "Otobüs bulunamadı."

    def OtobusBul(self, node, tarih, numara):
        if node is None:
            return None
        if node.tarih == tarih and node.numara == numara:
            return node
        elif tarih < node.tarih:
            return self.OtobusBul(node.left, tarih, numara)
        else:
            return self.OtobusBul(node.right, tarih, numara)

    def otobus_arama(self):
        otobusler = self.OtobusTarihleriniListele(self.root)
        if otobusler:
            print("\nOtobüslerin bulunduğu tarihler:")
            for i, tarih in enumerate(otobusler, 1):
                print("\n{}. {}".format(i,tarih))
            secim = int(input("\nBir tarih seçin (1-{}): ".format(len(otobusler))))
            if 1 <= secim <= len(otobusler):
                secilen_tarih = otobusler[secim - 1]
                otobusler = self.OtobusArama(self.root, secilen_tarih)
                return "\n".join(otobusler)
        return "Bu tarihte otobüs bulunamadı."

    def OtobusTarihleriniListele(self, node):
        if node is None:
            return []
        tarihler = []
        self._otobusTarihleriniListele_(node, tarihler)
        return sorted(set(tarihler))  # Tarihleri sıralamak için

    def _otobusTarihleriniListele_(self, node, tarihler):
        if node is None:
            return
        tarihler.append(node.tarih)
        self._otobusTarihleriniListele_(node.left, tarihler)
        self._otobusTarihleriniListele_(node.right, tarihler)

    def OtobusArama(self, node, tarih):
        if node is None:
            return []
        otobusler = []
        if node.tarih == tarih:
            otobusler.append(str(node))  # Otobüs detaylarını listelemek için
        otobusler.extend(self.OtobusArama(node.left, tarih))
        otobusler.extend(self.OtobusArama(node.right, tarih))
        return otobusler

    def yolcu_arama(self):
        otobusler = self.OtobusListele(self.root)
        if otobusler:
            print("\nMevcut otobüsler:\n")
            for i, otobus in enumerate(otobusler, 1):
                print("{}-) {} - {} numaralı otobüs".format(i,otobus.tarih,otobus.numara))
            secim = int(input("Bir otobüs seçin (1-{}): ".format(len(otobusler))))
            if 1 <= secim <= len(otobusler):
                secilen_otobus = otobusler[secim - 1]
                ad = input("Aradığınız yolcunun adını girin: ")
                soyad = input("Aradığınız yolcunun soyadını girin: ")
                return self.YolcuBul(secilen_otobus, ad, soyad)
        return "Yolcu bulunamadı."

    def OtobusListele(self, node):
        if node is None:
            return []
        otobusler = [node] 
        otobusler.extend(self.OtobusListele(node.left))
        otobusler.extend(self.OtobusListele(node.right))
        return otobusler

    def YolcuBul(self, otobus_node, ad, soyad):
        if otobus_node:
            for yolcu in otobus_node.yolcular:
                if yolcu.ad == ad and yolcu.soyad == soyad:
                    print("\nYolcu bulundu: {}".format(yolcu))
                    secim = input("1-) Yolcuyu Sil\n2-) Yolcuyu Güncelle\n3-) Çıkış\nSeçiminizi yapın: ")
                    if secim == '1':
                        if otobus_node.YolcuSil(ad, soyad):
                            print("{} {} yolcu başarıyla silindi.".format(ad, soyad))
                            return  
                    elif secim == '2':
                        yeni_ad = input("\nYeni adı girin: ")
                        yeni_soyad = input("Yeni soyadı girin: ")
                        otobus_node.YolcuGuncelle(ad, soyad, yeni_ad, yeni_soyad)
                        print("\nYolcu başarıyla güncellendi: {} {}".format(yeni_ad, yeni_soyad))
                        return  
                    elif secim == '3':
                        return  
                    else:
                        print("Geçerli bir seçim yapın.")
            print("Yolcu bulunamadı.")  


def tarih_belirleme():
    while True:
        gun = int(input("Otobüs tarihi için gün girin: "))
        if 1 <= gun <= 31:
            break
        else:
            print("Lütfen geçerli bir gün girin.")
            
    while True:
        ay = int(input("Otobüs tarihi için ay girin: "))
        if 1 <= ay <= 12:
            break
        else:
            print("Lütfen geçerli bir ay girin.")
            
    while True:
        yil = int(input("Otobüs tarihi için yıl girin: "))
        if yil >= 2024:
            break
        else:
            print("Lütfen geçerli bir yıl girin.")     
    return '-'.join([str(gun), str(ay), str(yil)])


# Kullanıcı arayüzü kısmı
sistem = OtobusYonetimSistemi()

while True:
    print("\n1. Otobüs Ekle")
    print("2. Yolcu Ekle")
    print("3. Otobüs Arama")
    print("4. Yolcu Arama")
    print("5. Çıkış")

    secim = input("Seçiminizi yapın (1-5): ")

    if secim == '1':
        # Otobüs ekleme
        tarih = tarih_belirleme()
        numara = input("Ekleyeceğiniz otobüs için otobüs numarasını girin: ")
        sistem.otobus_ekle(tarih, numara)
        print("\n{} tarihine {} numaralı otobüs eklendi.".format(tarih,numara))

    elif secim == '2':
        # Yolcu ekleme
        tarih = tarih_belirleme()
        numara = input("Yolcu eklemek için otobüs numarasını girin: ")
        ad = input("Yolcunun adını girin: ")
        soyad = input("Yolcunun soyadını girin: ")

        yolcu = Yolcu(ad, soyad)
        mesaj = sistem.yolcu_ekle(tarih, numara, yolcu)
        print(mesaj)

    elif secim == '3':
        # Otobüs arama
        otobusler = sistem.otobus_arama()
        print("\n{}".format(otobusler))
        

    elif secim == '4':
        # Yolcu arama
        mesaj = sistem.yolcu_arama()
        print(mesaj)

    elif secim == '5':
        print("Çıkılıyor...")
        break

    else:
        print("Geçersiz seçim, tekrar deneyin.")

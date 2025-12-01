
CREATE DATABASE QLQUANCAFE;
USE QLQUANCAFE;


CREATE TABLE MENU (
    MaMon INT PRIMARY KEY IDENTITY(1,1), 
    TenMon NVARCHAR(100) NOT NULL,
    Gia DECIMAL(10, 0) NOT NULL,
    Loai NVARCHAR(50)
);

INSERT INTO MENU (TenMon, Gia, Loai) VALUES
(N'Cà phê ðen ðá', 15000, N'Cà phê'),
(N'Trà ðào cam s?', 35000, N'Trà'),
(N'Bánh Tiramisu', 40000, N'Bánh'),
(N'Latte nóng', 45000, N'Cà phê');

SELECT * FROM MENU;

CREATE TABLE HOADON (
    MaHD INT PRIMARY KEY IDENTITY(1,1),           
    NgayLap DATETIME NOT NULL DEFAULT GETDATE(),
    MaBan NVARCHAR(10) NULL,                     
    TongTien DECIMAL(10, 0) DEFAULT 0
);

CREATE TABLE CHITIETHOADON (
    MaCTHD INT PRIMARY KEY IDENTITY(1,1),             
    MaHD INT NOT NULL,                                
    MaMon INT NOT NULL,                               
    SoLuong INT NOT NULL,
    DonGia DECIMAL(10, 0) NOT NULL,                   
    
   
    CONSTRAINT FK_CTHD_HOADON
        FOREIGN KEY (MaHD)
        REFERENCES HOADON (MaHD)
        ON DELETE CASCADE,  
    
    CONSTRAINT FK_CTHD_MENU
        FOREIGN KEY (MaMon)
        REFERENCES MENU (MaMon)
        ON DELETE NO ACTION 
);
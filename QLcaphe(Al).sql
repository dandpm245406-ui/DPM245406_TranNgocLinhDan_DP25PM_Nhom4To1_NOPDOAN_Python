CREATE DATABASE QLcaphe
USE QLcaphe
CREATE TABLE caphe (
    macaphe VARCHAR(30) PRIMARY KEY,
    tencaphe VARCHAR(30),
    loai VARCHAR(30),
    gia FLOAT,
    soluong INT,
    ngaynhap DATE,
    nhacungcap VARCHAR(30),
    maloai VARCHAR(30),
    
    FOREIGN KEY (maloai) REFERENCES loaicaphe(maloai)
);

CREATE TABLE loaicaphe (
    maloai VARCHAR(30) PRIMARY KEY,
    tenloai VARCHAR(30)
);

CREATE TABLE nhacungcap (
    mancc VARCHAR(30) PRIMARY KEY,
    tenncc VARCHAR(30),
    diachi VARCHAR(30)
);

ALTER TABLE caphe 
ADD mancc VARCHAR(30);

ALTER TABLE caphe
ADD FOREIGN KEY (mancc) REFERENCES nhacungcap(mancc);

INSERT INTO loaicaphe VALUES
('LC01', 'Robusta'),
('LC02', 'Arabica'),
('LC03', 'Culi');

INSERT INTO nhacungcap VALUES
('NCC01', 'Nhà cung cấp A', 'HCM'),
('NCC02', 'Nhà cung cấp B', 'HN'),
('NCC03', 'Nhà cung cấp C', 'Đà Nẵng');

COMMIT;


SHOW DATABASES; 
DROP DATABASE QLcaphe;
DROP DATABASE qlnhanvien;
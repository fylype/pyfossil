// ============================================================================
// Parâmetros da Geometria (edite livremente)
// ============================================================================
L  = 10.0;          // Comprimento (direção X)
W  =  5.0;          // Largura     (direção Y)
H  =  4.0;          // Altura      (direção Z)

R  =  1.0;          // Raio do poço (furo)

CX = L / 2.0;       // Centro X do poço
CY = W / 2.0;       // Centro Y do poço

// Número de camadas na direção Z
nLayersZ = 8;

// ============================================================================
// Parâmetros de Malha (controle de resolução)
// ============================================================================
lc_borda = 0.20;    // Tamanho característico nas bordas externas
lc_poco  = 0.05;    // Tamanho característico no contorno do poço (mais fino)

// ============================================================================
// 1. Pontos da base (z = 0)
// ============================================================================
// Retângulo externo
Point(1) = {0, 0, 0, lc_borda};
Point(2) = {L, 0, 0, lc_borda};
Point(3) = {L, W, 0, lc_borda};
Point(4) = {0, W, 0, lc_borda};

// Centro e pontos do círculo (poço)
Point(5) = {CX,     CY,     0, lc_poco};   // centro
Point(6) = {CX + R, CY,     0, lc_poco};   // direita
Point(7) = {CX,     CY + R, 0, lc_poco};   // cima
Point(8) = {CX - R, CY,     0, lc_poco};   // esquerda
Point(9) = {CX,     CY - R, 0, lc_poco};   // baixo

// ============================================================================
// 2. Linhas e arcos da base
// ============================================================================
// Contorno externo
Line(1) = {1, 2};   // Bottom  (y = 0)
Line(2) = {2, 3};   // Right   (x = L)
Line(3) = {3, 4};   // Top     (y = W)
Line(4) = {4, 1};   // Left    (x = 0)

// Arcos do poço
Circle(5) = {6, 5, 7};
Circle(6) = {7, 5, 8};
Circle(7) = {8, 5, 9};
Circle(8) = {9, 5, 6};

// ============================================================================
// 3. Superfície da base (com furo)
// ============================================================================
Curve Loop(1) = {1, 2, 3, 4};          // contorno externo
Curve Loop(2) = {5, 6, 7, 8};          // contorno do poço

Plane Surface(1) = {1, 2};             // superfície com furo

// ============================================================================
// 4. Extrusão na direção Z
// ============================================================================
out[] = Extrude {0, 0, H} {
  Surface{1};
  Layers{nLayersZ};
  Recombine;
};

// ============================================================================
// 5. Physical Groups – IDs compatíveis com o .prm do FOSSIL
// ============================================================================
// Volume
Physical Volume("Reservoir_Domain", 100) = {out[1]};

// ---------- Fronteiras (IDs 1 a 7) ----------
// Boundary 1 → Left_Open      (x = 0)
Physical Surface("Left_Open", 1) = {out[5]};

// Boundary 2 → Right_Open     (x = L)
Physical Surface("Right_Open", 2) = {out[3]};

// Boundary 3 → Bottom_NoFlow  (y = 0)  – face frontal
Physical Surface("Bottom_NoFlow", 3) = {out[2]};

// Boundary 4 → Top_NoFlow     (y = W)  – face traseira
Physical Surface("Top_NoFlow", 4) = {out[4]};

// Boundary 5 → Front_NoFlow   (z = 0)  – base
Physical Surface("Front_NoFlow", 5) = {1};

// Boundary 6 → Back_NoFlow    (z = H)  – topo
Physical Surface("Back_NoFlow", 6) = {out[0]};

// Boundary 7 → Injection_Hole (parede do poço)
Physical Surface("Injection_Hole", 7) = {out[6], out[7], out[8], out[9]};

// ============================================================================
// 6. Opções de malha
// ============================================================================
Mesh.Algorithm   = 6;          // Frontal-Delaunay
Mesh.Algorithm3D = 1;          // Delaunay
Mesh.RecombineAll = 1;

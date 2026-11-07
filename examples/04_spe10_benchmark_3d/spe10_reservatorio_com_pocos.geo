// ============================================================================
// BENCHMARK SPE 10 (MODELO 2) - MALHA SÓLIDA NÃO-ESTRUTURADA 3D COM LGR NOS POÇOS
// ============================================================================
// Domínio contínuo e fechado (SEM FUROS), correspondendo exatamente ao modelo
// geométrico SPE 10 Modelo 2 original (1200 ft x 2200 ft x 170 ft).
//
// Os poços são operados como poços padrão do FOSSIL (modelo de Peaceman via
// sim.well_set_config), enquanto a malha não-estruturada possui refinamento
// local adaptativo (LGR) automático em torno de cada poço:
//   - Células menores e densas nas posições do injetor e produtores
//   - Transição suave para células maiores no centro do reservatório
//   - Parâmetros independentes para o poço injetor e poços produtores
// ============================================================================

FT_TO_M = 0.3048;

// ============================================================================
// 1. Geometria do Reservatório SPE 10 (em metros)
// ============================================================================
L = 1200.0 * FT_TO_M;   // Comprimento (X): 1200 ft = 365.76 m
W = 2200.0 * FT_TO_M;   // Largura     (Y): 2200 ft = 670.56 m
H =  170.0 * FT_TO_M;   // Espessura   (Z):  170 ft =  51.816 m

// Número de camadas verticais na extrusão (direção Z)
// (Pode ser ajustado para 11, 17, 34 ou 85 camadas)
nLayersZ = 12;

// ============================================================================
// 2. Parâmetros de Refinamento do Poço Injetor Central (INJ1)
// ============================================================================
CX_inj = L / 2.0;       // Posição X do injetor (600 ft = 182.88 m)
CY_inj = W / 2.0;       // Posição Y do injetor (1100 ft = 335.28 m)

lc_inj       = 5.0 * FT_TO_M;   // Tamanho característico da célula no injetor (~1.52 m)
r_refine_inj = 50.0 * FT_TO_M;  // Raio de refinamento máximo ao redor do injetor (~15.24 m)
r_trans_inj  = 200.0 * FT_TO_M; // Raio de transição suave para a malha geral (~60.96 m)

// ============================================================================
// 3. Parâmetros de Refinamento dos Poços Produtores (P1, P2, P3, P4)
// ============================================================================
// Localização dos poços produtores nos 4 cantos:
// Use 0.0 para os cantos exatos (0,0), (L,0), (L,W), (0,W) ou
// especifique uma distância caso queira posicioná-los no centro da célula de canto
// (ex.: 10 ft e 5 ft, correspondendo a dx/2 e dy/2 da grade original do SPE10).
offset_prod_x = 0.0 * FT_TO_M;  // 0.0 para os cantos exatos (ou dx/2 para centro de célula)
offset_prod_y = 0.0 * FT_TO_M;  // 0.0 para os cantos exatos (ou dy/2 para centro de célula)

lc_prod       = 8.0 * FT_TO_M;   // Tamanho característico da célula nos produtores (~2.44 m)
r_refine_prod = 70.0 * FT_TO_M;  // Raio de refinamento máximo ao redor dos produtores (~21.34 m)
r_trans_prod  = 250.0 * FT_TO_M; // Raio de transição suave para a malha geral (~76.2 m)

// ============================================================================
// 4. Parâmetros da Malha de Campo Distante (Reservatório Geral)
// ============================================================================
lc_borda = 100.0 * FT_TO_M;       // Tamanho de elemento no miolo do reservatório (~15.24 m)


// ============================================================================
// 5. Pontos e Superfície da Base (z = 0)
// ============================================================================
Point(1) = {0, 0, 0, lc_borda};
Point(2) = {L, 0, 0, lc_borda};
Point(3) = {L, W, 0, lc_borda};
Point(4) = {0, W, 0, lc_borda};

Line(1) = {1, 2};   // Borda inferior (y = 0)
Line(2) = {2, 3};   // Borda direita  (x = L)
Line(3) = {3, 4};   // Borda superior (y = W)
Line(4) = {4, 1};   // Borda esquerda (x = 0)

Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};

// Ponto do Injetor Central (INJ1) para o cálculo de distância do campo de refinamento
Point(5) = {CX_inj, CY_inj, 0, lc_inj};

// Pontos dos Poços Produtores (para o campo de refinamento se houver deslocamento interno)
If (offset_prod_x > 0.0 || offset_prod_y > 0.0)
  Point(6) = {offset_prod_x,     offset_prod_y,     0, lc_prod};
  Point(7) = {L - offset_prod_x, offset_prod_y,     0, lc_prod};
  Point(8) = {L - offset_prod_x, W - offset_prod_y, 0, lc_prod};
  Point(9) = {offset_prod_x,     W - offset_prod_y, 0, lc_prod};
EndIf


// ============================================================================
// 6. Campos de Tamanho de Malha (Size Fields / LGR Adaptativo)
// ============================================================================
// --- 6.1 Refinamento ao redor do Poço Injetor Central ---
Field[1] = Distance;
Field[1].PointsList = {5};

Field[2] = Threshold;
Field[2].InField = 1;
Field[2].SizeMin = lc_inj;
Field[2].SizeMax = lc_borda;
Field[2].DistMin = r_refine_inj;
Field[2].DistMax = r_trans_inj;

// --- 6.2 Refinamento ao redor dos Poços Produtores ---
Field[3] = Distance;
If (offset_prod_x > 0.0 || offset_prod_y > 0.0)
  Field[3].PointsList = {6, 7, 8, 9};
Else
  Field[3].PointsList = {1, 2, 3, 4};
EndIf

Field[4] = Threshold;
Field[4].InField = 3;
Field[4].SizeMin = lc_prod;
Field[4].SizeMax = lc_borda;
Field[4].DistMin = r_refine_prod;
Field[4].DistMax = r_trans_prod;

// --- 6.3 Combinação (Mínimo entre os campos de injeção e produção) ---
Field[5] = Min;
Field[5].FieldsList = {2, 4};

Background Field = 5;


// ============================================================================
// 7. Extrusão na Direção Z (Geração do Volume 3D)
// ============================================================================
out[] = Extrude {0, 0, H} {
  Surface{1};
  Layers{nLayersZ};
  Recombine;
};


// ============================================================================
// 8. Grupos Físicos (Physical Groups para o FOSSIL / deal.II)
// ============================================================================
// Volume 3D do Reservatório
Physical Volume("Reservoir_Domain", 100) = {out[1]};

// Fronteiras Externas do Reservatório (IDs 1 a 6)
// Todas fechadas (No-Flow / Neumann nulo) no benchmark SPE 10
Physical Surface("Left_NoFlow",   1) = {out[5]};  // x = 0
Physical Surface("Right_NoFlow",  2) = {out[3]};  // x = L
Physical Surface("Bottom_NoFlow", 3) = {out[2]};  // y = 0
Physical Surface("Top_NoFlow",    4) = {out[4]};  // y = W
Physical Surface("Front_NoFlow",  5) = {1};       // z = 0 (base)
Physical Surface("Back_NoFlow",   6) = {out[0]};  // z = H (topo)


// ============================================================================
// 9. Opções de Algoritmo de Malha
// ============================================================================
Mesh.MshFileVersion = 2.2;     // Formato MSH 2.2 nativo e 100% suportado pelo deal.II
Mesh.Algorithm   = 6;          // Frontal-Delaunay para malha 2D de alta qualidade
Mesh.Algorithm3D = 1;          // Delaunay
Mesh.RecombineAll = 1;         // Recombina triângulos em quadriláteros na base
Mesh.RecombinationAlgorithm = 3; // Blossom Full-Quad (garante 100% quadriláteros, eliminando prismas/wedges tipo 6)
Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.MeshSizeFromCurvature = 0;

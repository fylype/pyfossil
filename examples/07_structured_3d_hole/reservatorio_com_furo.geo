// ============================================================================
// Parâmetros da Geometria
// ============================================================================
L  = 10.0;          // Comprimento (direção X)
W  =  5.0;          // Largura     (direção Y)
H  =  4.0;          // Altura      (direção Z)
R  =  1.0;          // Raio do poço (furo)

CX = L / 2.0;       // Centro X do poço
CY = W / 2.0;       // Centro Y do poço

nLayersZ = 8;       // Número de camadas na extrusão Z

// ============================================================================
// Parâmetros da Malha Estruturada (Transfinite)
// ============================================================================
// Em malhas estruturadas, controlamos o NÚMERO DE ELEMENTOS em cada aresta.
nCircX = 20;        // Elementos ao longo dos arcos superior/inferior (e bordas X)
nCircY = 15;        // Elementos ao longo dos arcos esquerdo/direito (e bordas Y)
nRadial = 15;       // Elementos radiais (conectando o poço à borda)

// Progressão Geométrica (1.15 = os elementos crescem 15% a cada passo 
// saindo do poço em direção à borda exterior)
radial_prog = 1.15; 

// ============================================================================
// 1. Pontos (Base Z = 0)
// ============================================================================
// Quinas do retângulo externo
Point(1) = {0, 0, 0};
Point(2) = {L, 0, 0};
Point(3) = {L, W, 0};
Point(4) = {0, W, 0};

// Centro do poço
Point(5) = {CX, CY, 0};

// Pontos na borda do poço (nas diagonais de 45 graus)
R_diag = R * Cos(Pi/4);
Point(6) = {CX - R_diag, CY - R_diag, 0};   // Inferior-Esquerda
Point(7) = {CX + R_diag, CY - R_diag, 0};   // Inferior-Direita
Point(8) = {CX + R_diag, CY + R_diag, 0};   // Superior-Direita
Point(9) = {CX - R_diag, CY + R_diag, 0};   // Superior-Esquerda

// ============================================================================
// 2. Curvas
// ============================================================================
// Bordas externas do retângulo
Line(1) = {1, 2};   // Inferior
Line(2) = {2, 3};   // Direita
Line(3) = {3, 4};   // Superior
Line(4) = {4, 1};   // Esquerda

// Arcos do poço (sentido anti-horário)
Circle(5) = {6, 5, 7}; // Arco Inferior
Circle(6) = {7, 5, 8}; // Arco Direito
Circle(7) = {8, 5, 9}; // Arco Superior
Circle(8) = {9, 5, 6}; // Arco Esquerdo

// Linhas Radiais: Conectando os cantos do furo aos cantos externos
// (Sentido = Furo -> Borda Externa)
Line(9)  = {6, 1};  // Diagonal IE
Line(10) = {7, 2};  // Diagonal ID
Line(11) = {8, 3};  // Diagonal SD
Line(12) = {9, 4};  // Diagonal SE

// ============================================================================
// 3. Superfícies (Formando a topologia "Butterfly" de 4 Blocos)
// ============================================================================
// Bloco 1: Inferior
Curve Loop(1) = {1, -10, -5, 9}; 
Plane Surface(1) = {1};

// Bloco 2: Direito
Curve Loop(2) = {2, -11, -6, 10}; 
Plane Surface(2) = {2};

// Bloco 3: Superior
Curve Loop(3) = {3, -12, -7, 11}; 
Plane Surface(3) = {3};

// Bloco 4: Esquerdo
Curve Loop(4) = {4, -9, -8, 12}; 
Plane Surface(4) = {4};

// ============================================================================
// 4. Mapeamento Transfinite (A mágica da estruturação em Quads)
// ============================================================================
// Define o número de elementos nas direções tangenciais e radiais
Transfinite Curve {1, 5, 3, 7} = nCircX;
Transfinite Curve {2, 6, 4, 8} = nCircY;

// As linhas radiais terão elementos pequenos perto do poço crescendo para fora
Transfinite Curve {9, 10, 11, 12} = nRadial Using Progression radial_prog;

// Define cada superfície como transfinita e força a recombinação em Quadriláteros
Transfinite Surface {1} = {1, 2, 7, 6}; Recombine Surface {1};
Transfinite Surface {2} = {2, 3, 8, 7}; Recombine Surface {2};
Transfinite Surface {3} = {3, 4, 9, 8}; Recombine Surface {3};
Transfinite Surface {4} = {4, 1, 6, 9}; Recombine Surface {4};

// ============================================================================
// 5. Extrusão em 3D (Gerando os Hexaedros)
// ============================================================================
// Extrude os 4 blocos simultaneamente. O Gmsh retornará vetores com os IDs.
out1[] = Extrude {0, 0, H} { Surface{1}; Layers{nLayersZ}; Recombine; };
out2[] = Extrude {0, 0, H} { Surface{2}; Layers{nLayersZ}; Recombine; };
out3[] = Extrude {0, 0, H} { Surface{3}; Layers{nLayersZ}; Recombine; };
out4[] = Extrude {0, 0, H} { Surface{4}; Layers{nLayersZ}; Recombine; };

// ============================================================================
// 6. Physical Groups para o FOSSIL
// ============================================================================
// Volume (Soma dos 4 blocos)
Physical Volume("Reservoir_Domain", 100) = {out1[1], out2[1], out3[1], out4[1]};

// Em Extrude do Gmsh: 
// [0] = Topo
// [1] = Volume
// [2] = Face gerada pela 1ª curva do Loop...
// [3] = Face gerada pela 2ª curva do Loop... e assim por diante.

// Boundary 1 → Left_Open      (Extrusão da Curva 4 no Loop 4)
Physical Surface("Left_Open", 1) = {out4[2]};

// Boundary 2 → Right_Open     (Extrusão da Curva 2 no Loop 2)
Physical Surface("Right_Open", 2) = {out2[2]};

// Boundary 3 → Bottom_NoFlow  (Extrusão da Curva 1 no Loop 1)
Physical Surface("Bottom_NoFlow", 3) = {out1[2]};

// Boundary 4 → Top_NoFlow     (Extrusão da Curva 3 no Loop 3)
Physical Surface("Top_NoFlow", 4) = {out3[2]};

// Boundary 5 → Front_NoFlow   (As 4 superfícies bases Z = 0)
Physical Surface("Front_NoFlow", 5) = {1, 2, 3, 4};

// Boundary 6 → Back_NoFlow    (As 4 superfícies topo Z = H)
Physical Surface("Back_NoFlow", 6) = {out1[0], out2[0], out3[0], out4[0]};

// Boundary 7 → Injection_Hole (Extrusão dos Arcos 5, 6, 7 e 8)
Physical Surface("Injection_Hole", 7) = {out1[4], out2[4], out3[4], out4[4]};

// ============================================================================
// 7. Opções de Exportação
// ============================================================================
Mesh.RecombineAll = 1;
Mesh.SubdivisionAlgorithm = 0; // Garante quads puros

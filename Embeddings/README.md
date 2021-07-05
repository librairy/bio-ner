# Embeddings

Use proposed model (BioBERT) for visualization of entity embeddings through TensorBoard Projector.

For this purpose a Jupyter Notebook (*Embeddings.ipynb*) is used to ease the processing and obtainment of the embeddings jointly with its subsequent visualization in PCA, t-SNE and UMAP graphs.
An example list with a set of terms of different semantic types is provided (Chemicals, Diseases, Genes, Proteins) -> *embeddings_test.txt*

## Dependencies

In addition to the dependencies related to the model, the following dependencies are needed for visualizing the embeddings:
  - TensorBoard
  - h5py
  
The python files used for processing the embeddings were obtained from its original implementation: [BioBERT](https://github.com/dmis-lab/biobert-pytorch)

## Results
The following visualizations were obtained through this embedding processing

 <img src="images/2d-pca.png" alt="Bidimensional PCA of examples"  width="250">  <img src="images/tsne.png" alt="3D t-SNE of examples"  width="250">  <img src="images/umap.png" alt="UMAP of examples"  width="250">  
 <img src="images/2dtsne_diseases.png" alt="2D t-SNE of disease examples"  width="500">

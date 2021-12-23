from data import Retriever, retrieve_class_names

def prepare_dataset():
    classes = retrieve_class_names()
    pages = Retriever().retrieve(classes)

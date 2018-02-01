if(system.graph("graph_stress").exists()) {
  system.graph("graph_stress").drop()
}
system.graph("graph_stress").create()
:remote config alias g graph_stress.g
schema.config().option('graph.schema_mode').set(com.datastax.bdp.graph.api.model.Schema.Mode.Production);

schema.propertyKey('summary').Text().single().create()
schema.propertyKey('timestampAsText').Text().single().create()
schema.propertyKey('answerType').Text().single().create()
schema.propertyKey('rating').Double().single().create()
schema.propertyKey('description').Text().single().create()
schema.propertyKey('title').Text().single().create()
schema.propertyKey('imUrl').Text().single().create()
schema.propertyKey('name').Text().single().create()
schema.propertyKey('answer').Text().single().create()
schema.propertyKey('price').Double().single().create()
schema.propertyKey('rank').Int().single().create()
schema.propertyKey('id').Text().single().create()
schema.propertyKey('helpful').Double().single().create()
schema.propertyKey('brand').Text().single().create()
schema.propertyKey('reviewText').Text().single().create()
schema.propertyKey('timestamp').Timestamp().single().create()


schema.vertexLabel('Item').partitionKey("id").properties('price', 'title', 'imUrl', 'description', 'brand').create()
schema.vertexLabel('Category').partitionKey('id').create()
schema.vertexLabel('Customer').partitionKey('id').properties('name').create()

schema.edgeLabel('viewed_with').connection('Item', 'Item').create()
schema.edgeLabel('also_bought').connection('Item', 'Item').create()
schema.edgeLabel('reviewed').properties('summary', 'reviewText', 'timestampAsText', 'timestamp', 'helpful', 'rating').connection('Customer', 'Item').create()
schema.edgeLabel('purchased_with').connection('Item', 'Item').create()
schema.edgeLabel('belongs_in_category').connection('Item', 'Category').create()
schema.edgeLabel('has_salesRank').properties('rank').connection('Item', 'Category').create()
schema.edgeLabel('bought_after_viewing').connection('Item', 'Item').create()

schema.vertexLabel('Item').index('byprice').materialized().by('price').add()
schema.vertexLabel('Customer').index('byrating').outE("reviewed").by('rating').add()
schema.vertexLabel('Item').index('byrank').outE("has_salesRank").by('rank').add()
schema.vertexLabel('Item').index('byhelpful').inE('reviewed').by('helpful').add()
schema.vertexLabel("Item").index("customer_review_by_rating").inE("reviewed").by("rating").add()

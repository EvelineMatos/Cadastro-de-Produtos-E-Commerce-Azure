SELECT TOP (100) [id]
      ,[nome]
      ,[descricao]
      ,[image_url]
      ,[preco]
  FROM [dbo].[produtos]


  SELECT * FROM [dbo].[produtos] WHERE [image_url] = '0';
   DELETE FROM [dbo].[produtos] WHERE [image_url] = '0';


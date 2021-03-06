USE [AdventureWorksDW2019]
GO
/****** Object:  Table [dbo].[customers]    Script Date: 4/4/2022 3:29:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[customers](
	[customerId] [int] IDENTITY(1,1) NOT NULL,
	[customername] [varchar](200) NOT NULL,
	[customertype] [varchar](20) NULL,
	[entrydate] [datetime] NOT NULL,
	[created_at] [datetime] NULL,
	[modified_at] [datetime] NULL,
 CONSTRAINT [PK_customers_pk] PRIMARY KEY CLUSTERED 
(
	[customerId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[fact_transactions]    Script Date: 4/4/2022 3:29:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[fact_transactions](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[customerId] [int] NULL,
	[productdescription] [varchar](300) NOT NULL,
	[quantity] [int] NULL,
	[sales] [money] NULL,
	[salesdate] [datetime] NULL,
	[created_at] [datetime] NULL,
	[modified_at] [datetime] NULL,
 CONSTRAINT [PK_fact_product_pk] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[customers] ON 

INSERT [dbo].[customers] ([customerId], [customername], [customertype], [entrydate], [created_at], [modified_at]) VALUES (1, N'Michael Scott', N'Corporate', CAST(N'2022-03-30T13:30:47.730' AS DateTime), CAST(N'2022-03-30T13:30:47.730' AS DateTime), CAST(N'2022-03-30T13:30:47.730' AS DateTime))
INSERT [dbo].[customers] ([customerId], [customername], [customertype], [entrydate], [created_at], [modified_at]) VALUES (2, N'Dwight Schrute', N'Individual', CAST(N'2022-03-30T13:31:29.650' AS DateTime), CAST(N'2022-03-30T13:31:29.650' AS DateTime), CAST(N'2022-03-30T13:31:29.650' AS DateTime))
INSERT [dbo].[customers] ([customerId], [customername], [customertype], [entrydate], [created_at], [modified_at]) VALUES (3, N'Jim Halpert', N'Individual', CAST(N'2022-03-30T13:31:46.090' AS DateTime), CAST(N'2022-03-30T13:31:46.090' AS DateTime), CAST(N'2022-03-30T17:08:39.050' AS DateTime))
SET IDENTITY_INSERT [dbo].[customers] OFF
GO
SET IDENTITY_INSERT [dbo].[fact_transactions] ON 

INSERT [dbo].[fact_transactions] ([Id], [customerId], [productdescription], [quantity], [sales], [salesdate], [created_at], [modified_at]) VALUES (1, 1, N'Bond paper', 2, 22.3400, CAST(N'2022-03-30T13:34:25.240' AS DateTime), CAST(N'2022-03-30T13:34:25.240' AS DateTime), CAST(N'2022-03-30T13:34:25.240' AS DateTime))
INSERT [dbo].[fact_transactions] ([Id], [customerId], [productdescription], [quantity], [sales], [salesdate], [created_at], [modified_at]) VALUES (2, 1, N'Gloss coated paper', 1, 11.3400, CAST(N'2022-03-30T13:35:38.057' AS DateTime), CAST(N'2022-03-30T13:35:38.057' AS DateTime), CAST(N'2022-03-30T13:35:38.057' AS DateTime))
INSERT [dbo].[fact_transactions] ([Id], [customerId], [productdescription], [quantity], [sales], [salesdate], [created_at], [modified_at]) VALUES (3, 2, N'Watermarked paper', 1, 8.3400, CAST(N'2022-03-30T13:36:16.440' AS DateTime), CAST(N'2022-03-30T13:36:16.440' AS DateTime), CAST(N'2022-03-30T13:36:16.440' AS DateTime))
INSERT [dbo].[fact_transactions] ([Id], [customerId], [productdescription], [quantity], [sales], [salesdate], [created_at], [modified_at]) VALUES (4, 1, N'Letter Envelop', 100, 18.3400, CAST(N'2022-03-31T13:39:22.970' AS DateTime), CAST(N'2022-03-31T13:39:22.970' AS DateTime), CAST(N'2022-03-31T13:39:22.970' AS DateTime))
INSERT [dbo].[fact_transactions] ([Id], [customerId], [productdescription], [quantity], [sales], [salesdate], [created_at], [modified_at]) VALUES (5, 3, N'BiC Round Stic', 60, 8.3400, CAST(N'2022-03-31T13:40:32.150' AS DateTime), CAST(N'2022-03-31T13:40:32.150' AS DateTime), CAST(N'2022-03-31T13:40:32.150' AS DateTime))
SET IDENTITY_INSERT [dbo].[fact_transactions] OFF
GO
ALTER TABLE [dbo].[customers] ADD  DEFAULT (getdate()) FOR [entrydate]
GO
ALTER TABLE [dbo].[customers] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[customers] ADD  DEFAULT (getdate()) FOR [modified_at]
GO
ALTER TABLE [dbo].[fact_transactions] ADD  DEFAULT (getdate()) FOR [salesdate]
GO
ALTER TABLE [dbo].[fact_transactions] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[fact_transactions] ADD  DEFAULT (getdate()) FOR [modified_at]
GO

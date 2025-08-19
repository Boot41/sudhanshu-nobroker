# Product
NoBroker app which is used to book a property for renting purpose.
The main USP of it is that a property owner can list a property and get tenants for it.
The tenants can apply for those properties.
Removes the high brokerage and broker problem.

# Main User Stories

## Core Experience
- As a user, I want a role-based landing page, so I see relevant content.
- As a tenant, I want to avoid brokers, so I don't pay unreasonable fees.

## Property Search & Discovery
- As an owner, I want to list properties, so tenants can view them.
- As a tenant, I want to filter by price and location, so I find suitable listings.
- As a tenant, I want to see amenities, so I know what’s included.
- As a tenant, I want photo galleries, so I can preview properties visually.
- As a tenant, I want to shortlist properties, so I can review them later.

## Application & Verification
- As a tenant, I want to apply to properties, so I can show interest.
- As a tenant, I want to schedule visits, so I can inspect properties.
- As a tenant, I want to track application status, so I know the progress.
- As a tenant, I want to upload documents, so owners can verify me.

## Post-Booking
- As a tenant, I want payment reminders, so I don't miss due dates.

# Unique Selling Propositions (USPs)
- **Direct Connections:** Connects property owners directly with tenants, eliminating the need for brokers.
- **Zero Brokerage:** Saves tenants money by removing brokerage fees entirely.
- **Simplified Process:** Streamlines the property search, application, and rental process through a single platform.




# UI Breakdown

## For Tenants (Looking for a Property)

### Pages
- **Home Page:** Features a prominent search bar, a list of featured properties, and easy navigation to other key sections.
- **Search Results Page:** Displays a list of properties based on search criteria, with options for filtering and sorting.
- **Property Details Page:** Shows comprehensive information about a single property, including a photo gallery, amenities, rent details, and an option to contact the owner.
- **Shortlisted Properties Page:** A personalized space where tenants can view all the properties they have saved for later.
- **My Applications Page:** A dashboard for tenants to track the status of their applications (e.g., Sent, Viewed, Accepted).

### Navigation
- **Bottom Tab Bar:** Provides quick access to Home, Shortlisted, My Applications, and Profile.

### Widgets
- **Property Card:** A reusable component for displaying property summaries in lists.
- **Filter Panel:** Allows users to refine search results by price, location, amenities, etc.
- **Image Gallery:** A carousel for viewing multiple property photos.
- **Scheduler:** A calendar interface for scheduling property visits with owners.

## For Property Owners

### Pages
- **Dashboard:** An overview of all listed properties, their status, and incoming inquiries.
- **Add/Edit Property Page:** A step-by-step form for owners to list a new property or update an existing one.
- **Inquiries Page:** A list of all applications from potential tenants.
- **Tenant Profile Viewer:** A page to view the details and documents of interested tenants.

### Navigation
- **Bottom Tab Bar:** Provides quick access to Dashboard, Inquiries, Add Property, and Profile.

# Future Stretch Goals

1.  **Virtual Property Tours:**
    -   **Description:** Allow property owners to upload 360-degree photos or videos to create virtual tours of their properties. Tenants can explore properties remotely, saving time for both parties.
    -   **User Journey Enhancement:** This enriches the property discovery phase for tenants, allowing them to shortlist properties with greater confidence before scheduling in-person visits.

2.  **Integrated Rental Agreements:**
    -   **Description:** Provide a feature to generate, digitally sign, and manage rental agreements directly within the app. This would include customizable templates and secure document storage.
    -   **User Journey Enhancement:** This streamlines the finalization stage of the rental process, making it faster, more secure, and entirely paperless for both tenants and owners.

3.  **Advanced Tenant Screening:**
    -   **Description:** Offer an automated screening service for property owners, which could include background checks and credit score verification (with tenant consent). This would help owners make more informed decisions.
    -   **User Journey Enhancement:** This adds a layer of trust and security for property owners, simplifying the tenant verification process and reducing risks.
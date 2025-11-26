import { faker } from '@faker-js/faker';

export interface User {
  email: string;
  name: string;
  password?: string;
  [key: string]: any;
}

export class UserFactory {
  private createdUsers: string[] = [];

  async createUser(overrides: Partial<User> = {}): Promise<User> {
    const user: User = {
      email: faker.internet.email(),
      name: faker.person.fullName(),
      password: faker.internet.password({ length: 12 }),
      ...overrides,
    };

    // In a real app, we would call the API here to seed the user.
    // For now, we mock the creation.
    // const response = await fetch(`${process.env.API_URL}/users`, ...);
    // this.createdUsers.push(created.id);
    
    console.log(`[Mock] Created user: ${user.email}`);
    this.createdUsers.push(user.email); // Tracking by email for mock
    
    return user;
  }

  async cleanup() {
    // Delete all created users
    if (this.createdUsers.length > 0) {
      console.log(`[Mock] Cleaning up ${this.createdUsers.length} users...`);
      // for (const userId of this.createdUsers) { ... delete ... }
      this.createdUsers = [];
    }
  }
}
